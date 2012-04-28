%
% SISG Class
%
% Copyright (c) 2012 Brian M Hunt

\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{sisg}[2012/04/25 SISG extension to the memoir class]

%
% Draft options
%
\DeclareOption*{%
	\PassOptionsToClass{\CurrentOption}{memoir}%
}


\ProcessOptions\relax

\LoadClass{memoir}

%\RequirePackage{alphalph,ifthen,multicol,ragged2e,zref-totpages,soul,%
%    graphicx,pdflscape,geometry,wallpaper,todonotes,,
%    }

\RequirePackage{xltxtra,lineno,hyperref,color,fontspec,xunicode}

%
% Draft
% 1: revision
%
\newcommand{\asdraft}[2]{
    % draft headers and footers
    \makeoddhead{SBC}{}%
        {%
            \color{Orange}\tiny \textbf{PRIVATE AND CONFIDENTIAL}
            – CONTENT NOT ENDORSED BY THE ILA, THE SISG OR ANY MEMBER THEREOF
        }{}

    \makeoddfoot{SBC}{\tiny Page \thepage~of \thelastpage}{}{%
        \color{Gray}\fbox{\tiny \parbox{1.75cm}{\centering rev. #1\\\today}}%
    }

    % Configure comment lines and line numbering
    \setlength{\textwidth}{0.618\textwidth}
    \def\PrintCommentLine{\kern1.1\textwidth\rule{0.618\textwidth}{1pt}}
    \def\makeLineNumberLeft{% 
      \hss\linenumberfont\LineNumber\hskip\linenumbersep%
      \hbox to 0pt{\PrintCommentLine\hss}}
    \linenumbers
    \leftlinenumbers
} % 'linenos' option



%
% Colors
%
\definecolor{DarkBlue}{RGB}{  23,  54,  93}
\definecolor{LightBlue}{RGB}{ 79, 129, 189}
\definecolor{Gray}{RGB}{     128, 128, 128}
\definecolor{Orange}{RGB}{   230, 145,  56}

%
% Title 
% 1: title name
%
\newcommand{\titlep}{
	\pagestyle{empty}%
	\vspace*{5.75cm}%
	{ % Title	
		\color{DarkBlue}%
		\headingfont%
		\large%
		\noindent{}%
		International Tribunal for State Financial Administration%
	}
} % \titlep

\newcommand{\subtitlep}[1]{
	\vspace{0.4cm}%
	{ % Subtitle
		\color{LightBlue}%
		\headingfont%
		\hrule{}%
		\vspace{0.8em}%
		\noindent{}%
		\textbf{#1}
	}
	\vfill%
	\begin{center}% Note at bottom of Cover page
        \small%
        \noindent{}%
        {\color{Gray}%
            Draft of the Sovereign Insolvency Study Group of the %
            International Law Association\newline{}%
        }\\\medskip%
        \textbf{WORKING COPY \textendash{} NOT FOR DISTRIBUTION}\\\bigskip%
	\end{center}
    \newpage%
    \noindent Copyright \copyright 2012 International Law Association.\par%
    %
    \medskip%
    % \includegraphics[scale=0.5]{cc-by.pdf}\par%
    \noindent%
    This work is licensed under a Creative Commons Attribution 3.0 Unported
    License. To view a copy of this license, visit
    \url{http://creativecommons.org/licenses/by/3.0/}
    or send a letter to Creative Commons, 171 Second Street, Suite 300,
    San Francisco, California, 94105, USA.\par%
    This edition was generated in PDF on \today.\par%
	\newpage%
    \tableofcontents*%
    \newpage%
	\pagestyle{SBC}% Presumably this is the old style of page
	\setcounter{page}{1}
} % \subtitlep


%
% Fonts
%
\defaultfontfeatures{Mapping=tex-text,Scale=MatchLowercase}
\setmainfont{Minion Pro}
\newfontfamily\headingfont{Minion Pro Semibold}
\newfontfamily\commentaryfont{Gentium Basic}

%
% Paragraph-fill limits for character-spacing
% \sloppy vs \fussy vs \midsloppy
% see memman.pdf p. 50
\midsloppy



%
% Par indents
%
\setlength{\parindent}{1em}

% Counters
% section # = article #
\counterwithout{section}{chapter}
\counterwithout{table}{chapter}
% 
\newcounter{sbc-article}
\setcounter{sbc-article}{1}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%           --- Headings --- 
%
%
% - Parts -
%   Tex style: \part
%   Color: Dark Blue
%   Left align
%   Large font
%   Reset section (article) number
\renewcommand{\chapnamefont}{\normalfont\headingfont%
    \large\color{DarkBlue}%
}

\renewcommand{\chaptitlefont}{\normalfont\headingfont%
    \large\color{DarkBlue}%
}

\renewcommand{\chapnumfont}{}
\renewcommand{\chaptername}{Part\space}

\def\chapternamenum{\chapnamefont\ }

\renewcommand*{\printchaptertitle}[1]{%
    \chaptitlefont #1\bigskip\hrule%
}

% see eg memman.pdf s. 6.3
%\renewcommand{\midchapskip}{\par\medskip}
%\renewcommand*{\beforechapskip}{\null\medskip}
%\renewcommand*{\afterchapskip}{\vskip\medskip}
\setlength{\midchapskip}{\baselineskip}
\setlength{\beforechapskip}{\baselineskip}
\setlength{\afterchapskip}{\baselineskip}

% No new page.
% \renewcommand*{\chappageend}{\medskip}

% - Articles -
%   Tex style: \section 
%   Color: Light blue
%   Cente
%   Regular font

% See memman p. 105ff
%\setsecnumformat{%
% \hspace{-\gutenNparindent}%
%    \textbf{\thesection{}.\space}%
%}
\newcounter{parnum}
\renewcommand*{\thesection}{Article \arabic{section}.}
\setsecheadstyle{\color{LightBlue}\bfseries\centering%
    \stepcounter{sbc-article}%
        \setcounter{parnum}{0}%
        \space%
}
% Hanging: see memman p. 106

% Commentary
\renewenvironment{quote}
{\begin{adjustwidth}{2em}{2em}\small\commentaryfont%
    \medskip\color{Gray}}
{\end{adjustwidth}}

% Table of Contents
% See memman p.156ff
% \renewcommand*{\cftchaptername}{\chaptername~}
\renewcommand*{\cftchaptername}{Part\space} % FIXME??
% \renewcommand*{\cftchaptername}{Chapter\space} % FIXME??

\renewcommand*{\cftsectionname}{}
\renewcommand*{\cftsectionaftersnum}{}

\renewcommand*{\cftsubsectionname}{} 
\renewcommand*{\cftsubsectionaftersnum}{.}

\cftsetindents{chapter}{3em}{3.2em}
\cftsetindents{section}{1em}{5.5em}
\cftsetindents{subsection}{1em}{5.5em}

\maxtocdepth{subsection}%
\setsecnumdepth{section}%

% Page styles
\copypagestyle{SBC}{plain}





% vim: set ft=tex
