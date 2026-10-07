r"""Insert the bibitems added by the 2026-10-07 reference audit into
paper_beyond_the_spectrum_3.tex, just before \end{thebibliography}.

Every entry below was resolved by refs_resolve.py (Crossref / DataCite / arXiv /
ISBN). The script is idempotent: it refuses to run if any new key is already present.
"""
from pathlib import Path

TEX = Path(__file__).resolve().parents[2] / "paper_beyond_the_spectrum_3.tex"

NEW = r"""
\bibitem{ArtsteinAvidanKarasevOstrover2014}
S.~Artstein-Avidan, R.~Karasev, and Y.~Ostrover,
\emph{From symplectic measurements to the Mahler conjecture},
Duke Mathematical Journal, \textbf{163} (2014), no.~11,
\href{https://doi.org/10.1215/00127094-2794999}{DOI: 10.1215/00127094-2794999}.

\bibitem{ArtsteinAvidanOstrover2008}
S.~Artstein-Avidan and Y.~Ostrover,
\emph{A Brunn--Minkowski inequality for symplectic capacities of convex domains},
International Mathematics Research Notices IMRN (2008), rnn044,
\href{https://doi.org/10.1093/imrn/rnn044}{DOI: 10.1093/imrn/rnn044}.

\bibitem{AkersRath2020}
C.~Akers and P.~Rath,
\emph{Entanglement wedge cross sections require tripartite entanglement},
Journal of High Energy Physics, \textbf{2020} (2020), no.~4, 208,
\href{https://doi.org/10.1007/JHEP04(2020)208}{DOI: 10.1007/JHEP04(2020)208}.

\bibitem{BelloniKawohlJuutinen2006}
M.~Belloni, B.~Kawohl, and P.~Juutinen,
\emph{The $p$-Laplace eigenvalue problem as $p\to\infty$ in a Finsler metric},
Journal of the European Mathematical Society, \textbf{8} (2006), no.~1, 123--138,
\href{https://doi.org/10.4171/JEMS/40}{DOI: 10.4171/JEMS/40}.

\bibitem{BlaberSivak2023}
S.~Blaber and D.~A. Sivak,
\emph{Optimal control in stochastic thermodynamics},
Journal of Physics Communications, \textbf{7} (2023), no.~3, 033001,
\href{https://doi.org/10.1088/2399-6528/acbf04}{DOI: 10.1088/2399-6528/acbf04}.

\bibitem{BoissonnatLieutierWintraecken2019}
J.-D. Boissonnat, A.~Lieutier, and M.~Wintraecken,
\emph{The reach, metric distortion, geodesic convexity and the variation of tangent spaces},
Journal of Applied and Computational Topology, \textbf{3} (2019), 29--58,
\href{https://doi.org/10.1007/s41468-019-00029-8}{DOI: 10.1007/s41468-019-00029-8}.

\bibitem{Carlson1963}
B.~C. Carlson,
\emph{Lauricella's hypergeometric function $F_D$},
Journal of Mathematical Analysis and Applications, \textbf{7} (1963), no.~3, 452--470,
\href{https://doi.org/10.1016/0022-247X(63)90067-2}{DOI: 10.1016/0022-247X(63)90067-2}.

\bibitem{ChampionDePascaleJimenez2008}
T.~Champion, L.~De~Pascale, and C.~Jimenez,
\emph{The $\infty$-eigenvalue problem and a problem of optimal transportation},
preprint (2008), arXiv:0811.1934,
\href{https://doi.org/10.48550/arXiv.0811.1934}{DOI: 10.48550/arXiv.0811.1934}.

\bibitem{Cheeger1970}
J.~Cheeger,
\emph{A lower bound for the smallest eigenvalue of the Laplacian},
in \emph{Problems in Analysis: A Symposium in Honor of Salomon Bochner}, Princeton University Press, Princeton, 1970, pp.~195--200,
\href{https://doi.org/10.1515/9781400869312-013}{DOI: 10.1515/9781400869312-013}.

\bibitem{Chow2022}
D.~D.~K. Chow,
\emph{Schl\"omilch integrals and probability distributions on the simplex},
preprint (2022), arXiv:2201.11013,
\href{https://doi.org/10.48550/arXiv.2201.11013}{DOI: 10.48550/arXiv.2201.11013}.

\bibitem{CieliebakHoferLatschevSchlenk2005}
K.~Cieliebak, H.~Hofer, J.~Latschev, and F.~Schlenk,
\emph{Quantitative symplectic geometry},
preprint (2005), arXiv:math/0506191,
\href{https://doi.org/10.48550/arXiv.math/0506191}{DOI: 10.48550/arXiv.math/0506191}.

\bibitem{Crooks2007}
G.~E. Crooks,
\emph{Measuring thermodynamic length},
Physical Review Letters, \textbf{99} (2007), no.~10, 100602,
\href{https://doi.org/10.1103/PhysRevLett.99.100602}{DOI: 10.1103/PhysRevLett.99.100602}.

\bibitem{DLMF}
F.~W.~J. Olver, D.~W. Lozier, R.~F. Boisvert, and C.~W. Clark (eds.),
\emph{NIST Handbook of Mathematical Functions},
Cambridge University Press, Cambridge, 2010, ISBN: 978-0-521-19225-5;
online as the \emph{NIST Digital Library of Mathematical Functions}, \url{https://dlmf.nist.gov}.

\bibitem{EkelandHofer1990}
I.~Ekeland and H.~Hofer,
\emph{Symplectic topology and Hamiltonian dynamics~II},
Mathematische Zeitschrift, \textbf{203} (1990), no.~1, 553--567,
\href{https://doi.org/10.1007/BF02570756}{DOI: 10.1007/BF02570756}.

\bibitem{FloerHofer1994}
A.~Floer and H.~Hofer,
\emph{Symplectic homology I: Open sets in $\mathbb{C}^n$},
Mathematische Zeitschrift, \textbf{215} (1994), no.~1, 37--88,
\href{https://doi.org/10.1007/BF02571699}{DOI: 10.1007/BF02571699}.

\bibitem{FukagaiItoNarukawa1999}
N.~Fukagai, M.~Ito, and K.~Narukawa,
\emph{Limit as $p\to\infty$ of $p$-Laplace eigenvalue problems and $L^\infty$-inequality of the Poincar\'e type},
Differential and Integral Equations, \textbf{12} (1999), no.~2, 183--206,
\href{https://doi.org/10.57262/die/1367265629}{DOI: 10.57262/die/1367265629}.

\bibitem{Gromov1985}
M.~Gromov,
\emph{Pseudo holomorphic curves in symplectic manifolds},
Inventiones Mathematicae, \textbf{82} (1985), no.~2, 307--347,
\href{https://doi.org/10.1007/BF01388806}{DOI: 10.1007/BF01388806}.

\bibitem{HaimKislevOstrover2026}
P.~Haim-Kislev and Y.~Ostrover,
\emph{A counterexample to Viterbo's conjecture},
Annals of Mathematics, \textbf{203} (2026), no.~2, 603--622,
\href{https://doi.org/10.4007/annals.2026.203.2.5}{DOI: 10.4007/annals.2026.203.2.5}.

\bibitem{HaydenLemmSorce2023}
P.~Hayden, M.~Lemm, and J.~Sorce,
\emph{Reflected entropy is not a correlation measure},
Physical Review A, \textbf{107} (2023), no.~5, L050401,
\href{https://doi.org/10.1103/PhysRevA.107.L050401}{DOI: 10.1103/PhysRevA.107.L050401}.

\bibitem{HaydenParrikarSorce2021}
P.~Hayden, O.~Parrikar, and J.~Sorce,
\emph{The Markov gap for geometric reflected entropy},
Journal of High Energy Physics, \textbf{2021} (2021), no.~10, 47,
\href{https://doi.org/10.1007/JHEP10(2021)047}{DOI: 10.1007/JHEP10(2021)047}.

\bibitem{JordanKinderlehrerOtto1998}
R.~Jordan, D.~Kinderlehrer, and F.~Otto,
\emph{The variational formulation of the Fokker--Planck equation},
SIAM Journal on Mathematical Analysis, \textbf{29} (1998), no.~1, 1--17,
\href{https://doi.org/10.1137/S0036141096303359}{DOI: 10.1137/S0036141096303359}.

\bibitem{Kashiwara1985}
M.~Kashiwara,
\emph{Index theorem for constructible sheaves},
Ast\'erisque, \textbf{130} (1985), 193--209,
\href{http://www.numdam.org/item?id=AST_1985__130__193_0}{Numdam: AST\_1985\_\_130\_\_193\_0}.

\bibitem{LiebRuskai1973}
E.~H. Lieb and M.~B. Ruskai,
\emph{Proof of the strong subadditivity of quantum-mechanical entropy},
Journal of Mathematical Physics, \textbf{14} (1973), no.~12, 1938--1941,
\href{https://doi.org/10.1063/1.1666274}{DOI: 10.1063/1.1666274}.

\bibitem{Lindqvist2008}
P.~Lindqvist,
\emph{A nonlinear eigenvalue problem},
in \emph{Topics in Mathematical Analysis}, Series on Analysis, Applications and Computation, World Scientific, Singapore, 2008, pp.~175--203,
ISBN: 978-981-281-105-9,
\href{https://doi.org/10.1142/9789812811066_0005}{DOI: 10.1142/9789812811066\_0005}.

\bibitem{MacPherson1974}
R.~D. MacPherson,
\emph{Chern classes for singular algebraic varieties},
Annals of Mathematics, \textbf{100} (1974), no.~2, 423--432,
\href{https://doi.org/10.2307/1971080}{DOI: 10.2307/1971080}.

\bibitem{Mather2012}
J.~Mather,
\emph{Notes on topological stability},
Bulletin of the American Mathematical Society, \textbf{49} (2012), no.~4, 475--506,
\href{https://doi.org/10.1090/S0273-0979-2012-01383-6}{DOI: 10.1090/S0273-0979-2012-01383-6}.

\bibitem{Mercer1909}
J.~Mercer,
\emph{Functions of positive and negative type, and their connection with the theory of integral equations},
Philosophical Transactions of the Royal Society of London, Series~A, \textbf{209} (1909), 415--446,
\href{https://doi.org/10.1098/rsta.1909.0016}{DOI: 10.1098/rsta.1909.0016}.

\bibitem{NakazatoIto2021}
M.~Nakazato and S.~Ito,
\emph{Geometrical aspects of entropy production in stochastic thermodynamics based on Wasserstein distance},
Physical Review Research, \textbf{3} (2021), no.~4, 043093,
\href{https://doi.org/10.1103/PhysRevResearch.3.043093}{DOI: 10.1103/PhysRevResearch.3.043093}.

\bibitem{NguyenEtAl2018}
P.~Nguyen, T.~Devakul, M.~G. Halbasch, M.~P. Zaletel, and B.~Swingle,
\emph{Entanglement of purification: from spin chains to holography},
Journal of High Energy Physics, \textbf{2018} (2018), no.~1, 98,
\href{https://doi.org/10.1007/JHEP01(2018)098}{DOI: 10.1007/JHEP01(2018)098}.

\bibitem{NiyogiSmaleWeinberger2008}
P.~Niyogi, S.~Smale, and S.~Weinberger,
\emph{Finding the homology of submanifolds with high confidence from random samples},
Discrete \& Computational Geometry, \textbf{39} (2008), 419--441,
\href{https://doi.org/10.1007/s00454-008-9053-2}{DOI: 10.1007/s00454-008-9053-2}.

\bibitem{OrroTrotman2010}
P.~Orro and D.~Trotman,
\emph{Regularity of the transverse intersection of two regular stratifications},
in \emph{Real and Complex Singularities}, London Mathematical Society Lecture Note Series, vol.~380, Cambridge University Press, Cambridge, 2010, pp.~298--304,
ISBN: 978-0-521-16969-1,
\href{https://doi.org/10.1017/CBO9780511731983.022}{DOI: 10.1017/CBO9780511731983.022}.

\bibitem{RatajZahle2019}
J.~Rataj and M.~Z\"ahle,
\emph{Curvature Measures of Singular Sets},
Springer Monographs in Mathematics, Springer, Cham, 2019,
ISBN: 978-3-030-18182-6,
\href{https://doi.org/10.1007/978-3-030-18183-3}{DOI: 10.1007/978-3-030-18183-3}.

\bibitem{SalamonBerry1983}
P.~Salamon and R.~S. Berry,
\emph{Thermodynamic length and dissipated availability},
Physical Review Letters, \textbf{51} (1983), no.~13, 1127--1130,
\href{https://doi.org/10.1103/PhysRevLett.51.1127}{DOI: 10.1103/PhysRevLett.51.1127}.

\bibitem{Schapira1991}
P.~Schapira,
\emph{Operations on constructible functions},
Journal of Pure and Applied Algebra, \textbf{72} (1991), no.~1, 83--93,
\href{https://doi.org/10.1016/0022-4049(91)90131-K}{DOI: 10.1016/0022-4049(91)90131-K}.

\bibitem{Schapira2017}
P.~Schapira,
\emph{Microlocal analysis and beyond},
preprint (2017), arXiv:1701.08955,
\href{https://doi.org/10.48550/arXiv.1701.08955}{DOI: 10.48550/arXiv.1701.08955}.

\bibitem{SchmiedlSeifert2007}
T.~Schmiedl and U.~Seifert,
\emph{Optimal finite-time processes in stochastic thermodynamics},
Physical Review Letters, \textbf{98} (2007), no.~10, 108301,
\href{https://doi.org/10.1103/PhysRevLett.98.108301}{DOI: 10.1103/PhysRevLett.98.108301}.

\bibitem{Schmidt1907}
E.~Schmidt,
\emph{Zur Theorie der linearen und nichtlinearen Integralgleichungen. I.~Teil},
Mathematische Annalen, \textbf{63} (1907), no.~4, 433--476,
\href{https://doi.org/10.1007/BF01449770}{DOI: 10.1007/BF01449770}.

\bibitem{Schwarz2000}
M.~Schwarz,
\emph{On the action spectrum for closed symplectically aspherical manifolds},
Pacific Journal of Mathematics, \textbf{193} (2000), no.~2, 419--461,
\href{https://doi.org/10.2140/pjm.2000.193.419}{DOI: 10.2140/pjm.2000.193.419}.

\bibitem{Seifert2012}
U.~Seifert,
\emph{Stochastic thermodynamics, fluctuation theorems and molecular machines},
Reports on Progress in Physics, \textbf{75} (2012), no.~12, 126001,
\href{https://doi.org/10.1088/0034-4885/75/12/126001}{DOI: 10.1088/0034-4885/75/12/126001}.

\bibitem{silvafilho2026book}
R.~M. Silva-Filho,
\emph{Geometry, Tensors, and Quantum Gravity},
monograph, Zenodo (2026),
\href{https://doi.org/10.5281/zenodo.22290043}{DOI: 10.5281/zenodo.22290043}.

\bibitem{Srednicki1993}
M.~Srednicki,
\emph{Entropy and area},
Physical Review Letters, \textbf{71} (1993), no.~5, 666--669,
\href{https://doi.org/10.1103/PhysRevLett.71.666}{DOI: 10.1103/PhysRevLett.71.666}.

\bibitem{Talagrand1996}
M.~Talagrand,
\emph{Transportation cost for Gaussian and other product measures},
Geometric and Functional Analysis, \textbf{6} (1996), no.~3, 587--600,
\href{https://doi.org/10.1007/BF02249265}{DOI: 10.1007/BF02249265}.

\bibitem{Trotman2020}
D.~Trotman,
\emph{Stratification theory},
in \emph{Handbook of Geometry and Topology of Singularities~I}, Springer, Cham, 2020, pp.~243--273,
ISBN: 978-3-030-53060-0,
\href{https://doi.org/10.1007/978-3-030-53061-7_4}{DOI: 10.1007/978-3-030-53061-7\_4}.

\bibitem{UmemotoTakayanagi2018}
K.~Umemoto and T.~Takayanagi,
\emph{Entanglement of purification through holographic duality},
Nature Physics, \textbf{14} (2018), no.~6, 573--577,
\href{https://doi.org/10.1038/s41567-018-0075-2}{DOI: 10.1038/s41567-018-0075-2}.

\bibitem{VanVuSaito2023}
T.~Van~Vu and K.~Saito,
\emph{Thermodynamic unification of optimal transport: thermodynamic uncertainty relation, minimum dissipation, and thermodynamic speed limits},
Physical Review X, \textbf{13} (2023), no.~1, 011013,
\href{https://doi.org/10.1103/PhysRevX.13.011013}{DOI: 10.1103/PhysRevX.13.011013}.

\bibitem{Villani2009}
C.~Villani,
\emph{Optimal Transport: Old and New},
Grundlehren der mathematischen Wissenschaften, vol.~338, Springer, Berlin, Heidelberg, 2009,
ISBN: 978-3-540-71049-3,
\href{https://doi.org/10.1007/978-3-540-71050-9}{DOI: 10.1007/978-3-540-71050-9}.

\bibitem{Viro1988}
O.~Y. Viro,
\emph{Some integral calculus based on Euler characteristic},
in \emph{Topology and Geometry --- Rohlin Seminar}, Lecture Notes in Mathematics, vol.~1346, Springer, Berlin, Heidelberg, 1988, pp.~127--138,
ISBN: 978-3-540-50237-1,
\href{https://doi.org/10.1007/BFb0082775}{DOI: 10.1007/BFb0082775}.

\bibitem{Viterbo1992}
C.~Viterbo,
\emph{Symplectic topology as the geometry of generating functions},
Mathematische Annalen, \textbf{292} (1992), no.~1, 685--710,
\href{https://doi.org/10.1007/BF01444643}{DOI: 10.1007/BF01444643}.

\bibitem{Viterbo2000}
C.~Viterbo,
\emph{Metric and isoperimetric problems in symplectic geometry},
Journal of the American Mathematical Society, \textbf{13} (2000), no.~2, 411--431,
\href{https://doi.org/10.1090/S0894-0347-00-00328-3}{DOI: 10.1090/S0894-0347-00-00328-3}.

\bibitem{vonRenesseSturm2005}
M.-K. von~Renesse and K.-T. Sturm,
\emph{Transport inequalities, gradient estimates, entropy and Ricci curvature},
Communications on Pure and Applied Mathematics, \textbf{58} (2005), no.~7, 923--940,
\href{https://doi.org/10.1002/cpa.20060}{DOI: 10.1002/cpa.20060}.

\bibitem{Weyl1939}
H.~Weyl,
\emph{On the volume of tubes},
American Journal of Mathematics, \textbf{61} (1939), no.~2, 461--472,
\href{https://doi.org/10.2307/2371513}{DOI: 10.2307/2371513}.

\bibitem{Whitney1965}
H.~Whitney,
\emph{Tangents to an analytic variety},
Annals of Mathematics, \textbf{81} (1965), no.~3, 496--549,
\href{https://doi.org/10.2307/1970400}{DOI: 10.2307/1970400}.

\bibitem{ZhongDeWeese2024}
A.~Zhong and M.~R. DeWeese,
\emph{Beyond linear response: equivalence between thermodynamic geometry and optimal transport},
Physical Review Letters, \textbf{133} (2024), no.~5, 057102,
\href{https://doi.org/10.1103/PhysRevLett.133.057102}{DOI: 10.1103/PhysRevLett.133.057102}.
"""


def main() -> None:
    tex = TEX.read_text(encoding="utf-8")
    import re
    new_keys = re.findall(r"\\bibitem\{([^}]+)\}", NEW)
    clash = [k for k in new_keys if "\\bibitem{" + k + "}" in tex]
    if clash:
        raise SystemExit(f"refusing: keys already present: {clash}")
    marker = "\n\\end{thebibliography}"
    assert tex.count(marker) == 1
    tex = tex.replace(marker, NEW.rstrip() + "\n" + marker)
    TEX.write_text(tex, encoding="utf-8")
    print(f"inserted {len(new_keys)} bibitems")


if __name__ == "__main__":
    main()
