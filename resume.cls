% Resume class adapted for single-page resumes
\ProvidesClass{resume}[2025/02/26 Simple resume class]
\NeedsTeXFormat{LaTeX2e}
\LoadClass{article}

\makeatletter
% Packages
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{mathptmx}
\RequirePackage{geometry}
\RequirePackage{titlesec}
\RequirePackage{enumitem}
\RequirePackage{hyperref}

% Page layout
\geometry{left=0.6in,right=0.6in,top=0.4in,bottom=0.4in}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlist[itemize]{leftmargin=1.5em,noitemsep,topsep=2pt}

% Name and address macros
\def\name#1{\def\@name{#1}}
\def\@name{}
\def\address#1{\def\@address{#1}}
\def\@address{}

% Header formatting
\newcommand{\printheader}{%
  {\LARGE\bfseries\@name}\par
  \@address\par
  \vspace{4pt}\par
}

% Section formatting
\titleformat{\section}{\large\bfseries}{}{0pt}{}
\titlespacing*{\section}{0pt}{6pt}{4pt}

\newenvironment{rSection}[1]{
  \sectionskip
  \section*{#1}\vspace{-4pt}
  \hrule height 0.6pt\vspace{4pt}
  \begin{list}{}{\setlength{\leftmargin}{0pt}\setlength{\itemsep}{4pt}}}
  {\end{list}}

\newenvironment{rSubsection}[4]{
  {\bfseries #1} \hfill {#2}\\
  {#3} \hfill {#4}
  \begin{itemize}}
  {\end{itemize}}

% Vertical spacing helper
\newcommand{\sectionskip}{\vspace{4pt}}

\hypersetup{colorlinks=true,linkcolor=black,urlcolor=black}
\makeatother
