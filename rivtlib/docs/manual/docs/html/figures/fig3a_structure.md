%!PS-Adobe-3.0 EPSF-3.0
%%Creator: Mayura Draw, Version 4.5
%%Title: fig3a_structure.md
%%CreationDate: Mon Jun 30 01:31:08 2014
%%BoundingBox: 25 280 535 615
%%DocumentFonts: Arial-BoldMT
%%+ ArialMT
%%Orientation: Portrait
%%EndComments
%%BeginProlog
%%BeginResource: procset MayuraDraw_ops
%%Version: 4.5
%%Copyright: (c) 1993-2003 Mayura Software
/PDXDict 100 dict def
PDXDict begin
% width height matrix proc key cache
% definepattern -\> font
/definepattern { %def
  7 dict begin
    /FontDict 9 dict def
    FontDict begin
      /cache exch def
      /key exch def
      /proc exch cvx def
      /mtx exch matrix invertmatrix def
      /height exch def
      /width exch def
      /ctm matrix currentmatrix def
      /ptm matrix identmatrix def
      /str
      (xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)
      def
    end
    /FontBBox [ %def
      0 0 FontDict /width get
      FontDict /height get
    ] def
    /FontMatrix FontDict /mtx get def
    /Encoding StandardEncoding def
    /FontType 3 def
    /BuildChar { %def
      pop begin
      FontDict begin
        width 0 cache { %ifelse
          0 0 width height setcachedevice
        }{ %else
          setcharwidth
        } ifelse
        0 0 moveto width 0 lineto
        width height lineto 0 height lineto
        closepath clip newpath
        gsave proc grestore
      end end
    } def
    FontDict /key get currentdict definefont
  end
} bind def

% dict patternpath -
% dict matrix patternpath -
/patternpath { %def
  dup type /dicttype eq { %ifelse
    begin FontDict /ctm get setmatrix
  }{ %else
    exch begin FontDict /ctm get setmatrix
    concat
  } ifelse
  currentdict setfont
  FontDict begin
    FontMatrix concat
    width 0 dtransform
    round width div exch round width div exch
    0 height dtransform
    round height div exch
    round height div exch
    0 0 transform round exch round exch
    ptm astore setmatrix

    pathbbox
    height div ceiling height mul 4 1 roll
    width div ceiling width mul 4 1 roll
    height div floor height mul 4 1 roll
    width div floor width mul 4 1 roll

    2 index sub height div ceiling cvi exch
    3 index sub width div ceiling cvi exch
    4 2 roll moveto

    FontMatrix ptm invertmatrix pop
    { %repeat
      gsave
        ptm concat
        dup str length idiv { %repeat
          str show
        } repeat
        dup str length mod str exch
        0 exch getinterval show
      grestore
      0 height rmoveto
    } repeat
    pop
  end end
} bind def

% dict patternfill -
% dict matrix patternfill -
/patternfill { %def
  gsave
    eoclip patternpath
  grestore
  newpath
} bind def

/img { %def
  gsave
  /imgh exch def
  /imgw exch def
  concat
  imgw imgh 8
  [imgw 0 0 imgh neg 0 imgh]
  /colorstr 768 string def
  /colorimage where {
    pop
    { currentfile colorstr readhexstring pop }
    false 3 colorimage
  }{
    /graystr 256 string def
    {
      currentfile colorstr readhexstring pop
      length 3 idiv
      dup 1 sub 0 1 3 -1 roll
      {
        graystr exch
        colorstr 1 index 3 mul get 30 mul
        colorstr 2 index 3 mul 1 add get 59 mul
        colorstr 3 index 3 mul 2 add get 11 mul
        add add 100 idiv
        put
      } for
      graystr 0 3 -1 roll getinterval
    } image
  } ifelse
  grestore
} bind def

/arrowhead {
  gsave
    [] 0 cmdDash
    strokeC strokeM strokeY strokeK setcmykcolor
    2 copy moveto
    4 2 roll exch 4 -1 roll exch
    sub 3 1 roll sub
    exch atan rotate dup scale
    arrowtype
    dup 0 eq {
      -1 2 rlineto 7 -2 rlineto -7 -2 rlineto
      closepath fill
    } if
    dup 1 eq {
      0 3 rlineto 9 -3 rlineto -9 -3 rlineto
      closepath fill
    } if
    dup 2 eq {
      -6 -6 rmoveto 6 6 rlineto -6 6 rlineto
      -1.4142 -1.4142 rlineto 4.5858 -4.5858 rlineto
      -4.5858 -4.5858 rlineto closepath fill
    } if
    dup 3 eq {
      -6 0 rmoveto -1 2 rlineto 7 -2 rlineto -7 -2 rlineto
      closepath fill
    } if
    dup 4 eq {
      -9 0 rmoveto 0 3 rlineto 9 -3 rlineto -9 -3 rlineto
      closepath fill
    } if
    dup 5 eq {
      currentpoint newpath 3 0 360 arc
      closepath fill
    } if
    dup 6 eq {
      2.5 2.5 rmoveto 0 -5 rlineto -5 0 rlineto 0 5 rlineto
      closepath fill
    } if
    pop
  grestore
} bind def

/setcmykcolor where { %ifelse
  pop
}{ %else
  /setcmykcolor {
     /black exch def /yellow exch def
     /magenta exch def /cyan exch def
     cyan black add dup 1 gt { pop 1 } if 1 exch sub
     magenta black add dup 1 gt { pop 1 } if 1 exch sub
     yellow black add dup 1 gt { pop 1 } if 1 exch sub
     setrgbcolor
  } bind def
} ifelse

/RE { %def
  findfont begin
  currentdict dup length dict begin
    { %forall
      1 index /FID ne { def } { pop pop } ifelse
    } forall
    /FontName exch def dup length 0 ne { %if
      /Encoding Encoding 256 array copy def
      0 exch { %forall
        dup type /nametype eq { %ifelse
          Encoding 2 index 2 index put
          pop 1 add
        }{ %else
          exch pop
        } ifelse
      } forall
    } if pop
  currentdict dup end end
  /FontName get exch definefont pop
} bind def

/spacecount { %def
  0 exch
  ( ) { %loop
    search { %ifelse
      pop 3 -1 roll 1 add 3 1 roll
    }{ pop exit } ifelse
  } loop
} bind def

/WinAnsiEncoding [
  39/quotesingle 96/grave 130/quotesinglbase/florin/quotedblbase
  /ellipsis/dagger/daggerdbl/circumflex/perthousand
  /Scaron/guilsinglleft/OE 145/quoteleft/quoteright
  /quotedblleft/quotedblright/bullet/endash/emdash
  /tilde/trademark/scaron/guilsinglright/oe/dotlessi
  159/Ydieresis 164/currency 166/brokenbar 168/dieresis/copyright
  /ordfeminine 172/logicalnot 174/registered/macron/ring
  177/plusminus/twosuperior/threesuperior/acute/mu
  183/periodcentered/cedilla/onesuperior/ordmasculine
  188/onequarter/onehalf/threequarters 192/Agrave/Aacute
  /Acircumflex/Atilde/Adieresis/Aring/AE/Ccedilla
  /Egrave/Eacute/Ecircumflex/Edieresis/Igrave/Iacute
  /Icircumflex/Idieresis/Eth/Ntilde/Ograve/Oacute
  /Ocircumflex/Otilde/Odieresis/multiply/Oslash
  /Ugrave/Uacute/Ucircumflex/Udieresis/Yacute/Thorn
  /germandbls/agrave/aacute/acircumflex/atilde/adieresis
  /aring/ae/ccedilla/egrave/eacute/ecircumflex
  /edieresis/igrave/iacute/icircumflex/idieresis
  /eth/ntilde/ograve/oacute/ocircumflex/otilde
  /odieresis/divide/oslash/ugrave/uacute/ucircumflex
  /udieresis/yacute/thorn/ydieresis
] def

/SymbolEncoding [
  32/space/exclam/universal/numbersign/existential/percent
  /ampersand/suchthat/parenleft/parenright/asteriskmath/plus
  /comma/minus/period/slash/zero/one/two/three/four/five/six
  /seven/eight/nine/colon/semicolon/less/equal/greater/question
  /congruent/Alpha/Beta/Chi/Delta/Epsilon/Phi/Gamma/Eta/Iota
  /theta1/Kappa/Lambda/Mu/Nu/Omicron/Pi/Theta/Rho/Sigma/Tau
  /Upsilon/sigma1/Omega/Xi/Psi/Zeta/bracketleft/therefore
  /bracketright/perpendicular/underscore/radicalex/alpha
  /beta/chi/delta/epsilon/phi/gamma/eta/iota/phi1/kappa/lambda
  /mu/nu/omicron/pi/theta/rho/sigma/tau/upsilon/omega1/omega
  /xi/psi/zeta/braceleft/bar/braceright/similar
  161/Upsilon1/minute/lessequal/fraction/infinity/florin/club
  /diamond/heart/spade/arrowboth/arrowleft/arrowup/arrowright
  /arrowdown/degree/plusminus/second/greaterequal/multiply
  /proportional/partialdiff/bullet/divide/notequal/equivalence
  /approxequal/ellipsis/arrowvertex/arrowhorizex/carriagereturn
  /aleph/Ifraktur/Rfraktur/weierstrass/circlemultiply
  /circleplus/emptyset/intersection/union/propersuperset
  /reflexsuperset/notsubset/propersubset/reflexsubset/element
  /notelement/angle/gradient/registerserif/copyrightserif
  /trademarkserif/product/radical/dotmath/logicalnot/logicaland
  /logicalor/arrowdblboth/arrowdblleft/arrowdblup/arrowdblright
  /arrowdbldown/lozenge/angleleft/registersans/copyrightsans
  /trademarksans/summation/parenlefttp/parenleftex/parenleftbt
  /bracketlefttp/bracketleftex/bracketleftbt/bracelefttp
  /braceleftmid/braceleftbt/braceex
  241/angleright/integral/integraltp/integralex/integralbt
  /parenrighttp/parenrightex/parenrightbt/bracketrighttp
  /bracketrightex/bracketrightbt/bracerighttp/bracerightmid
  /bracerightbt
] def

/patarray [
/leftdiagonal /rightdiagonal /crossdiagonal /horizontal
/vertical /crosshatch /fishscale /wave /brick
] def
/arrowtype 0 def
/fillC 0 def /fillM 0 def /fillY 0 def /fillK 0 def
/strokeC 0 def /strokeM 0 def /strokeY 0 def /strokeK 1 def
/pattern -1 def
/mat matrix def
/mat2 matrix def
/nesting 0 def
/deferred /N def
/c /curveto load def
/c2 { pop pop c } bind def
/C /curveto load def
/C2 { pop pop C } bind def
/e { gsave concat 0 0 moveto } bind def
/F {
  nesting 0 eq { %ifelse
    pattern -1 eq { %ifelse
      fillC fillM fillY fillK setcmykcolor eofill
    }{ %else
      gsave fillC fillM fillY fillK setcmykcolor eofill grestore
      0 0 0 1 setcmykcolor
      patarray pattern get findfont patternfill
    } ifelse
  }{ %else
    /deferred /F def
  } ifelse
} bind def
/f { closepath F } bind def
/K { /strokeK exch def /strokeY exch def
     /strokeM exch def /strokeC exch def } bind def
/k { /fillK exch def /fillY exch def
     /fillM exch def /fillC exch def } bind def
/opc { pop } bind def
/Opc { pop } bind def
/L /lineto load def
/L2 { pop pop L } bind def
/m /moveto load def
/m2 { pop pop m } bind def
/n /newpath load def
/N {
  nesting 0 eq { %ifelse
    newpath
  }{ %else
    /deferred /N def
  } ifelse
} def
/S {
  nesting 0 eq { %ifelse
    strokeC strokeM strokeY strokeK setcmykcolor stroke
  }{ %else
    /deferred /S def
  } ifelse
} bind def
/s { closepath S } bind def
/Tx { fillC fillM fillY fillK setcmykcolor show
      0 leading neg translate 0 0 moveto } bind def
/T { grestore } bind def
/TX { pop } bind def
/Ts { pop } bind def
/tal { pop } bind def
/tld { pop } bind def
/tbx { pop exch pop sub /jwidth exch def } def
/tpt { %def
  fillC fillM fillY fillK setcmykcolor
  moveto show
} bind def
/tpj { %def
  fillC fillM fillY fillK setcmykcolor
  moveto
  dup stringwidth pop
  3 -1 roll
  exch sub
  1 index spacecount
  dup 0 eq { %ifelse
    pop pop show
  }{ %else
    div 0 8#040 4 -1 roll widthshow
  } ifelse
} bind def
/u {} def
/U {} def
/*u { /nesting nesting 1 add def } def
/*U {
  /nesting nesting 1 sub def
  nesting 0 eq {
    deferred cvx exec
  } if
} def
/w /setlinewidth load def
/d /cmdDash load def
/B {
  nesting 0 eq { %ifelse
    gsave F grestore S
  }{ %else
    /deferred /B def
  } ifelse
} bind def
/b { closepath B } bind def
/z { /align exch def pop /leading exch def exch findfont
     exch scalefont setfont } bind def
/tfn { exch findfont
     exch scalefont setfont } bind def
/Pat { /pattern exch def } bind def
/cm { 6 array astore concat } bind def
/q { mat2 currentmatrix pop } bind def
/Q { mat2 setmatrix } bind def
/Ah {
  pop /arrowtype exch def
  currentlinewidth 5 1 roll arrowhead
} bind def
/Arc {
  mat currentmatrix pop
    translate scale 0 0 1 5 -2 roll arc
  mat setmatrix
} bind def
/Arc2 { pop pop Arc } bind def
/Bx {
  mat currentmatrix pop
    concat /y1 exch def /x1 exch def /y2 exch def /x2 exch def
    x1 y1 moveto x1 y2 lineto x2 y2 lineto x2 y1 lineto
  mat setmatrix
} bind def
/Rr {
  mat currentmatrix pop
    concat /yrad exch def /xrad exch def
    2 copy gt { exch } if /x2 exch def /x1 exch def
    2 copy gt { exch } if /y2 exch def /y1 exch def
    x1 xrad add y2 moveto
    matrix currentmatrix x1 xrad add y2 yrad sub translate xrad yrad scale
    0 0 1 90 -180 arc setmatrix
    matrix currentmatrix x1 xrad add y1 yrad add translate xrad yrad scale
    0 0 1 180 270 arc setmatrix
    matrix currentmatrix x2 xrad sub y1 yrad add translate xrad yrad scale
    0 0 1 270 0 arc setmatrix
    matrix currentmatrix x2 xrad sub y2 yrad sub translate xrad yrad scale
    0 0 1 0 90 arc setmatrix
    closepath
  mat setmatrix
} bind def
/Ov {
  mat currentmatrix pop
    concat translate scale 1 0 moveto 0 0 1 0 360 arc closepath
  mat setmatrix
} bind def
end
%%EndResource
%%EndProlog
%%BeginSetup
%PDX g 5 5 0 1
%%IncludeFont: Arial-BoldMT
%%IncludeFont: ArialMT
PDXDict begin
%%EndSetup
%%Page: 1 1
%%BeginPageSetup
/_PDX_savepage save def

15 15 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 setlinecap
  7.5 0 moveto 15 7.5 lineto
  0 7.5 moveto 7.5 15 lineto
  2 setlinewidth stroke
} bind
/rightdiagonal true definepattern pop

15 15 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 setlinecap
  7.5 0 moveto 0 7.5 lineto
  15 7.5 moveto 7.5 15 lineto
  2 setlinewidth stroke
} bind
/leftdiagonal true definepattern pop

15 15 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 setlinecap
  0 7.5 moveto 15 7.5 lineto
  2 setlinewidth stroke
} bind
/horizontal true definepattern pop

15 15 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 setlinecap
  7.5 0 moveto 7.5 15 lineto
  2 setlinewidth stroke
} bind
/vertical true definepattern pop

15 15 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 setlinecap
  0 7.5 moveto 15 7.5 lineto
  7.5 0 moveto 7.5 15 lineto
  2 setlinewidth stroke
} bind
/crosshatch true definepattern pop

30 30 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 setlinecap
  0 7.5 moveto 30 7.5 lineto
  0 22.5 moveto 30 22.5 lineto
  7.5 0 moveto 7.5 7.5 lineto
  7.5 22.5 moveto 7.5 30 lineto
  22.5 7.5 moveto 22.5 22.5 lineto
  1 setlinewidth stroke
} bind
/brick true definepattern pop

30 30 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 2 scale
  2 setlinecap
  7.5 0 moveto 15 7.5 lineto
  0 7.5 moveto 7.5 15 lineto
  7.5 0 moveto 0 7.5 lineto
  15 7.5 moveto 7.5 15 lineto
  0.5 setlinewidth stroke
} bind
/crossdiagonal true definepattern pop

30 30 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  2 2 scale
  1 setlinecap
  0 7.5 moveto 0 15 7.5 270 360 arc
  7.5 15 moveto 15 15 7.5 180 270 arc
  0 7.5 moveto 7.5 7.5 7.5 180 360 arc
  0.5 setlinewidth stroke
} bind
/fishscale true definepattern pop

30 30 [300 72 div 0 0 300 72 div 0 0]
{ %definepattern
  1 setlinecap 0.5 setlinewidth
  7.5 0 10.6 135 45 arcn
  22.5 15 10.6 225 315 arc
  stroke
  7.5 15 10.6 135 45 arcn
  22.5 30 10.6 225 315 arc
  stroke
} bind
/wave true definepattern pop

WinAnsiEncoding /_Arial-BoldMT /Arial-BoldMT RE
WinAnsiEncoding /_ArialMT /ArialMT RE

newpath 2 setlinecap 0 setlinejoin 2 setmiterlimit
[] 0 cmdDash
25 280 moveto 25 615 lineto 535 615 lineto 535 280 lineto closepath clip
newpath
%%EndPageSetup
0.5 w
470 470 355 545 [1 0 0 1 55 -170] Bx
b
485 340 370 535 [1 0 0 1 40 40] Bx
b
[1 0 0 1 -30 200] e
549.244 334.786 445 365 tbx
1 tal
15 tld
0.8 1 0.4 0 k
/_Arial-BoldMT 14 tfn
(Calc Set) 469.5 352.33 tpt
( ) TX
/_Arial-BoldMT 12 tfn
(LaTeX-PDF File) 453.112 337.33 tpt
T
-1.42109e-016 -1.42109e-016 -1.42109e-016 0 k
490 460 290 500 [1 0 0 1 -235 -125] Bx
b
[1 0 0 1 -150 -50] e
270 415 270 415 tbx
0 tal
15 tld
0.8 1 0.4 0 k
/_Arial-BoldMT 14 tfn
(Model File) 270 402.33 tpt
T
-1.42109e-016 -1.42109e-016 -1.42109e-016 0 k
400 295 200 490 [1 0 0 1 -145 85] Bx
b
0.431373 0.431373 0.431373 0 k
375 225 195 320 [1 0 0 1 -130 170] Bx
b
u
0.470588 0.466667 0.47451 0 k
300 255 215 300 [1 0 0 1 -140 145] Bx
b
[1 0 0 1 -145 85] e
235 355 235 355 tbx
0 tal
11 tld
0.729412 0.647059 0.25098 0 k
/_Arial-BoldMT 10 tfn
(EQUATION) 235 345.95 tpt
T
0.215686 0.223529 0.239216 0 k
235 250 200 270 [1 0 0 1 -120 155] Bx
b
[1 0 0 1 -145 160] e
230 260 230 260 tbx
0 tal
9 tld
0.807843 0.54902 0.760784 0 k
/_Arial-BoldMT 8 tfn
(TERM) 230 252.76 tpt
T
0.215686 0.223529 0.239216 0 k
235 250 200 270 [1 0 0 1 -80 155] Bx
b
[1 0 0 1 -105 160] e
230 260 230 260 tbx
0 tal
9 tld
0.807843 0.54902 0.760784 0 k
/_Arial-BoldMT 8 tfn
(TERM) 230 252.76 tpt
T
U
[1 0 0 1 -70 130] e
235 355 235 355 tbx
0 tal
17 tld
0.0352941 0.0352941 0.0352941 0 k
/_Arial-BoldMT 16 tfn
(SECTION) 235 340.52 tpt
T
0.470588 0.466667 0.47451 0 k
285 270 215 300 [1 0 0 1 -50 130] Bx
b
[1 0 0 1 -65 65] e
235 355 235 355 tbx
0 tal
11 tld
0.729412 0.647059 0.25098 0 k
/_Arial-BoldMT 10 tfn
(FUNCTIONS) 235 345.95 tpt
T
0.470588 0.466667 0.47451 0 k
285 270 215 300 [1 0 0 1 -50 165] Bx
b
[1 0 0 1 -65 100] e
235 355 235 355 tbx
0 tal
11 tld
0.729412 0.647059 0.25098 0 k
/_Arial-BoldMT 10 tfn
(EQUATIONS) 235 345.95 tpt
T
u
0.443137 0.443137 0.443137 0 k
280 330 200 355 [1 0 0 1 -135 170] Bx
b
[1 0 0 1 -165 165] e
235 355 235 355 tbx
0 tal
17 tld
0.0196078 0.027451 0.0392157 0 k
/_Arial-BoldMT 16 tfn
(SECTION) 235 340.52 tpt
T
0.431373 0.431373 0.431373 0 k
280 330 200 355 [1 0 0 1 -35 170] Bx
b
[1 0 0 1 -65 165] e
235 355 235 355 tbx
0 tal
17 tld
0.0196078 0.027451 0.0392157 0 k
/_Arial-BoldMT 16 tfn
(SECTION) 235 340.52 tpt
T
U
[1 0 0 1 -185 145] e
270 415 270 415 tbx
0 tal
15 tld
1 1 0.4 0 k
/_Arial-BoldMT 14 tfn
(Model File Contains) 270 402.33 tpt
T
[1 0 0 1 -200 120] e
385 485 385 485 tbx
0 tal
19 tld
1 1 1 0 k
/_Arial-BoldMT 18 tfn
(ASCII INPUTS) 385 468.71 tpt
T
[1 0 0 1 -170 185] e
595 420 595 420 tbx
0 tal
19 tld
/_Arial-BoldMT 18 tfn
(OUTPUTS) 595 403.71 tpt
T
-1.42109e-016 -1.42109e-016 -1.42109e-016 0 k
480 265 390 505 [1 0 0 1 -105 70] Bx
b
[1 0 0 1 -340 240] e
670 330 670 330 tbx
1 tal
15 tld
0.8 1 0.4 0 k
/_Arial-BoldMT 14 tfn
(Project) 646.27 317.33 tpt
(\r) TX
( File ) 654.047 302.33 tpt
(\r) TX
(Contains) 640.054 287.33 tpt
T
0.443137 0.443137 0.443137 0 k
0.0431373 0.0431373 0.0431373 0 K
575 390 480 440 [1 0 0 1 -60 -75] Bx
b
[1 0 0 1 -25 -15] e
545.02 326.713 445 375 tbx
1 tal
12 tld
1 1 0.4 0 k
/_Arial-BoldMT 11 tfn
(Single Calc File) 454.354 365.045 tpt
0.0862745 0.0862745 0.0862745 0 k
() 535.666 365.045 tpt
(\r) TX
(LaTeX-PDF) 465.673 353.045 tpt
(\r) TX
(or UTF-8) 472.4 341.045 tpt
(\r) TX
() 495.01 329.045 tpt
T
u
0.458824 0.458824 0.458824 0 k
580 410 485 435 [1 0 0 1 -65 -20] Bx
b
[1 0 0 1 -50 35] e
565 362.713 470 375 tbx
1 tal
12 tld
0.0862745 0.0862745 0.0862745 0 k
/_Arial-BoldMT 11 tfn
(Calc Document) 477.466 365.045 tpt
T
U
0.443137 0.443137 0.443137 0 k
585 380 505 430 [1 0 0 1 -215 20] Bx
b
[1 0 0 1 -210 70] e
580 322.596 500 375 tbx
1 tal
13 tld
0.054902 0.054902 0.054902 0 k
/_Arial-BoldMT 12 tfn
(file list and ) 506.988 364.14 tpt
(\r) TX
(formatting) 510.336 351.14 tpt
(\r) TX
(instructions) 505.662 338.14 tpt
(\r) TX
() 540 325.14 tpt
T
0.443137 0.443137 0.443137 0 k
585 390 505 435 [1 0 0 1 -215 75] Bx
b
[1 0 0 1 -210 125] e
580 348.596 500 375 tbx
1 tal
13 tld
0.054902 0.054902 0.054902 0 k
/_Arial-BoldMT 12 tfn
(project) 519.996 364.14 tpt
(\r) TX
(information) 507 351.14 tpt
T
u
0.458824 0.458824 0.458824 0 k
580 410 485 435 [1 0 0 1 -65 50] Bx
b
[1 0 0 1 -50 105] e
565 362.713 470 375 tbx
1 tal
12 tld
0.0862745 0.0862745 0.0862745 0 k
/_Arial-BoldMT 11 tfn
(Calc Document) 477.466 365.045 tpt
T
U
u
0.458824 0.458824 0.458824 0 k
580 410 485 435 [1 0 0 1 -65 15] Bx
b
[1 0 0 1 -50 70] e
565 362.713 470 375 tbx
1 tal
12 tld
0.0862745 0.0862745 0.0862745 0 k
/_Arial-BoldMT 11 tfn
(Calc Document) 477.466 365.045 tpt
T
U
[1 0 0 1 0 0] e
120 355 120 355 tbx
0 tal
13 tld
1 1 1 0 k
/_ArialMT 12 tfn
() 120 344.14 tpt
T
-1.42109e-016 -1.42109e-016 -1.42109e-016 0 k
1 1 1 0 K
490 460 290 500 [1 0 0 1 -235 -170] Bx
b
[1 0 0 1 -150 -95] e
270 415 270 415 tbx
0 tal
15 tld
0.8 1 0.4 0 k
/_Arial-BoldMT 14 tfn
(Model File) 270 402.33 tpt
T
0.443137 0.443137 0.443137 0 k
0.0431373 0.0431373 0.0431373 0 K
585 395 505 430 [1 0 0 1 -215 -45] Bx
b
[1 0 0 1 -210 5] e
580 335.596 500 375 tbx
1 tal
13 tld
0.054902 0.054902 0.054902 0 k
/_Arial-BoldMT 12 tfn
(calc template) 501.984 364.14 tpt
(\r) TX
(file name) 513.99 351.14 tpt
(\r) TX
() 540 338.14 tpt
T
u
0.458824 0.458824 0.458824 0 k
580 410 485 435 [1 0 0 1 -65 85] Bx
b
[1 0 0 1 -50 140] e
565 362.713 470 375 tbx
1 tal
12 tld
0.0862745 0.0862745 0.0862745 0 k
/_Arial-BoldMT 11 tfn
(Table of Contents) 471.052 365.045 tpt
T
U
-1.42109e-016 -1.42109e-016 -1.42109e-016 0 k
1 1 1 0 K
1 w
q
1 0 0 1 5 0 cm
260 310 m
398 310 400 310 L2
Q
S
q
1 0 0 1 5 0 cm
260 310 400 310 2 2 Ah
Q
q
1 0 0 1 -125 45 cm
385 310 m
398 310 400 310 L2
Q
S
q
1 0 0 1 -125 45 cm
385 310 400 310 2 2 Ah
Q
q
1 0 0 1 -125 155 cm
385 310 m
398 310 400 310 L2
Q
S
q
1 0 0 1 -125 155 cm
385 310 400 310 2 2 Ah
Q
q
1 0 0 1 0 135 cm
385 310 m
398 310 400 310 L2
Q
S
q
1 0 0 1 0 135 cm
385 310 400 310 2 2 Ah
Q
q
1 0 0 1 -350 185 cm
385 310 m
398 310 400 310 L2
Q
S
q
1 0 0 1 -350 185 cm
385 310 400 310 2 2 Ah
Q
q
1 0 0 1 0 0 cm
35 495 m
35 355 L
Q
S
q
1 0 0 1 0 5 cm
35 350 m
50 350 L
Q
S
0.470588 0.466667 0.47451 0 k
0.5 w
295 270 210 300 [1 0 0 1 -135 180] Bx
b
[1 0 0 1 -140 120] e
235 355 235 355 tbx
0 tal
11 tld
0.807843 0.909804 0.294118 0 k
/_Arial-BoldMT 10 tfn
(TEXT AND) 235 345.95 tpt
(\r) TX
(FIGURES) 235 334.95 tpt
T
%%PageTrailer
_PDX_savepage restore
%%Trailer
end
showpage
%%EOF
