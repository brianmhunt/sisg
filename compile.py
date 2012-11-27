#!/usr/bin/env python2.7
"""
Requires:
"""
import logging, argparse, os, os.path, sys, subprocess, codecs, hashlib

documents = {
        'treaty': ["brianmhunt@gmail.com:/all/all/", "SBG Treaty 2012"],
        }

with open(".gcp-pw.txt") as gpw:
    gcp_pw  = gpw.read()

author  = "International Law Association"
template= "pandoc.latex"

gcpcmd  = ['python', 'gcp.py', '-u', '-o', '-f', 'txt', '-p', gcp_pw]

pdcmd   = ['pandoc', '-t', 'latex', '--chapters', '--template', template, 
    '-V', "author=%s" % author]

texcmd  = ['xelatex']


def get_doc(doc):
    """Get latest version of the document"""
    user, gdocid = documents[doc]
    
    cmd = gcpcmd + ["%s%s" % (user, gdocid), "./docs"]

    print "Running: %s" % cmd
    rc = subprocess.call(cmd)

    # os.rename("%s.txt" % gdocid, doc) # eg SISG Treaty 2012.txt => treaty.txt

def run_pandoc(doc):
    """
    Take the original file ("docs/gdocid.txt") and create a new file
    doc.txt that has the parameters removed. Passed the variables in the head of
    the original file as arguments to pandoc
    """
    user, gdocid = documents[doc]

    doc_path = "./docs/%s.txt" % gdocid

    headers = {}
    body    = ""
    
    with codecs.open(doc_path, 'r', 'utf8') as of:
        # Note [1:] -- we skip the BOM: 
        # http://en.wikipedia.org/wiki/Byte_Order_Mark
        line = of.readline().strip()[1:]

        # variables
        while (line):
            name, value = line.split(":")
            headers[name.strip()] = value.strip()
            line = of.readline().strip()

        more = of.read()

        while (more):
            body += more
            more = of.read()


    # make build directory
    try:
        os.mkdir("build")
    except Exception:
        pass

    # save the body (MarkDown) to the build directory
    md_path = "build/%s.md" % doc
    with codecs.open(md_path, "w", "utf8") as of:
        of.write(body)

    # Compile the command & arguments
    cmd = pdcmd
    value_args = ["%s=%s" % (n.lower(), v) for n, v in headers.items()]
    for v in value_args:
        cmd += ["-V", v]

    # get a version number for this production
    version_file = "docs/%s.version.txt" % doc # keeps a list of md5's
    last_md5 = ""
    try:
        with open(version_file) as of:
            lines = of.readlines()
            version = len(lines)
            last_md5 = lines[-1].strip()
    except IOError:
        version = 0
        pass

    h = hashlib.new("md5")
    h.update("\n".join([]))
    h.update(body.encode('utf8'))
    current_md5 = h.hexdigest()

    if last_md5 != current_md5: # only a new version when files are different
        version = version + 1
        logging.info("New version found [%s]: %s" % (current_md5, version))

        with open(version_file, "a") as of:
            of.write("%s\n" % current_md5)
    else:
        logging.info("No changes to version [%s]: %s" % (current_md5, version))

    cmd += ["-V", "version=%s" % version]

    cmd += [md_path]
    cmd += ["-o", "build/%s.tex" % doc]

    logging.info("Running command: [%s]" % " ".join(cmd))

    rc = subprocess.call(cmd)

def run_latex(doc):
    os.chdir("build")
    cmd = texcmd + [doc]

    rc = subprocess.call(cmd)
    rc = subprocess.call(cmd) # insert TOC, page numbers, etc.

def build(doc):
    get_doc(doc)
    run_pandoc(doc)
    run_latex(doc)

def _get_parser():
    "Return the argument parser"
    parser = argparse.ArgumentParser()

    parser.add_argument("cmd", help="Command (get, pandoc, latex, build)")
    parser.add_argument("doc", help="Document (%s)" 
            % ", ".join(documents.keys()))

    return parser

commands = {
        "get"       : get_doc,
        "pandoc"    : run_pandoc,
        "latex"     : run_latex,
        "build"     : build
        }


if __name__ == '__main__':
    p = _get_parser()

    opts = p.parse_args()

    commands[opts.cmd](opts.doc)
    
