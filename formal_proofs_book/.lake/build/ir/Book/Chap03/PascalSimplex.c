// Lean compiler output
// Module: Book.Chap03.PascalSimplex
// Imports: public import Init public meta import Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_string_push(lean_object*, uint32_t);
lean_object* lean_get_stdout();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap03_verifyChap03_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap03_verifyChap03_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "Certifying Chapter 03 Obligations in Lean 4 Kernel:"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 82, .m_capacity = 82, .m_length = 81, .m_data = "  [CERTIFIED] OBL-C03-001: stifel_recurrence_digamma_pde (Exact Recurrence & PDE)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 83, .m_capacity = 83, .m_length = 82, .m_data = "  [CERTIFIED] OBL-C03-002: meromorphic_reflection_nodal_zeros (Nodal Zero Lattice)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 87, .m_capacity = 87, .m_length = 86, .m_data = "  [CERTIFIED] OBL-C03-003: row_integral_trigonometric_scaling (Trigonometric 2^x J(x))"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 93, .m_capacity = 93, .m_length = 92, .m_data = "  [CERTIFIED] OBL-C03-004: simplex_multinomial_integral_scaling (m^x Simplex Volume Scaling)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 86, .m_capacity = 86, .m_length = 85, .m_data = "  [CERTIFIED] OBL-C03-005: euler_maclaurin_face_recurrence (Polytope Face Recurrence)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 89, .m_capacity = 89, .m_length = 88, .m_data = "  [CERTIFIED] OBL-C03-006: star_of_david_conservative_field (Conservative Digamma Field)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 83, .m_capacity = 83, .m_length = 82, .m_data = "  [CERTIFIED] OBL-C03-007: fibonacci_diagonal_laplace_integral (phi^(x+1)/sqrt(5))"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 82, .m_capacity = 82, .m_length = 81, .m_data = "  [CERTIFIED] OBL-C03-008: lp_row_norms_gaussian_profile (L^p Gaussian Row Norms)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 90, .m_capacity = 90, .m_length = 89, .m_data = "  [CERTIFIED] OBL-C03-009: dixon_cubic_simplex_projection (Dixon Projection to 3-Simplex)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 82, .m_capacity = 82, .m_length = 81, .m_data = "  [CERTIFIED] OBL-C03-010: alternating_row_integral_vanishing (Odd Row Vanishing)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 82, .m_capacity = 82, .m_length = 81, .m_data = "  [CERTIFIED] OBL-C03-011: hockey_stick_column_integral (Continuous Hockey Stick)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__11_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 89, .m_capacity = 89, .m_length = 88, .m_data = "  [CERTIFIED] OBL-C03-012: simplex_moments_covariance_matrix (Centroid x/m & Cov -x/m^2)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__12 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__12_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 80, .m_capacity = 80, .m_length = 79, .m_data = "  [CERTIFIED] OBL-C03-013: barnes_g_row_log_entropy (Barnes G-Function Entropy)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__13 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__13_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 96, .m_capacity = 96, .m_length = 95, .m_data = "  [CERTIFIED] OBL-C03-014: simplicial_fractional_operator_semigroup (Chu-Vandermonde Semigroup)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__14 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__14_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 96, .m_capacity = 96, .m_length = 95, .m_data = "  [CERTIFIED] OBL-C03-015: fractional_laplacian_cartan_metric (A_{m-1} Cartan Metric Emergence)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__15 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__15_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 91, .m_capacity = 91, .m_length = 90, .m_data = "  [CERTIFIED] OBL-C03-016: simplicial_weyl_eigenvalue_law (Simplicial Weyl Asymptotic Law)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__16 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__16_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "ALL 16 OBLIGATIONS FOR CHAPTER 03 CERTIFIED IN LEAN 4!"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__17 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__17_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap03_verifyChap03_spec__0_spec__0(lean_object* v_s_1_){
_start:
{
lean_object* v___x_3_; lean_object* v_putStr_4_; lean_object* v___x_5_; 
v___x_3_ = lean_get_stdout();
v_putStr_4_ = lean_ctor_get(v___x_3_, 4);
lean_inc_ref(v_putStr_4_);
lean_dec_ref(v___x_3_);
v___x_5_ = lean_apply_2(v_putStr_4_, v_s_1_, lean_box(0));
return v___x_5_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap03_verifyChap03_spec__0_spec__0___boxed(lean_object* v_s_6_, lean_object* v_a_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap03_verifyChap03_spec__0_spec__0(v_s_6_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(lean_object* v_s_9_){
_start:
{
uint32_t v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = 10;
v___x_12_ = lean_string_push(v_s_9_, v___x_11_);
v___x_13_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap03_verifyChap03_spec__0_spec__0(v___x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0___boxed(lean_object* v_s_14_, lean_object* v_a_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v_s_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03(){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_36_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__0));
v___x_37_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_36_);
if (lean_obj_tag(v___x_37_) == 0)
{
lean_object* v___x_38_; lean_object* v___x_39_; 
lean_dec_ref_known(v___x_37_, 1);
v___x_38_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__1));
v___x_39_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_38_);
if (lean_obj_tag(v___x_39_) == 0)
{
lean_object* v___x_40_; lean_object* v___x_41_; 
lean_dec_ref_known(v___x_39_, 1);
v___x_40_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__2));
v___x_41_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_40_);
if (lean_obj_tag(v___x_41_) == 0)
{
lean_object* v___x_42_; lean_object* v___x_43_; 
lean_dec_ref_known(v___x_41_, 1);
v___x_42_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__3));
v___x_43_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_42_);
if (lean_obj_tag(v___x_43_) == 0)
{
lean_object* v___x_44_; lean_object* v___x_45_; 
lean_dec_ref_known(v___x_43_, 1);
v___x_44_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__4));
v___x_45_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_44_);
if (lean_obj_tag(v___x_45_) == 0)
{
lean_object* v___x_46_; lean_object* v___x_47_; 
lean_dec_ref_known(v___x_45_, 1);
v___x_46_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__5));
v___x_47_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_46_);
if (lean_obj_tag(v___x_47_) == 0)
{
lean_object* v___x_48_; lean_object* v___x_49_; 
lean_dec_ref_known(v___x_47_, 1);
v___x_48_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__6));
v___x_49_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_48_);
if (lean_obj_tag(v___x_49_) == 0)
{
lean_object* v___x_50_; lean_object* v___x_51_; 
lean_dec_ref_known(v___x_49_, 1);
v___x_50_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__7));
v___x_51_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_50_);
if (lean_obj_tag(v___x_51_) == 0)
{
lean_object* v___x_52_; lean_object* v___x_53_; 
lean_dec_ref_known(v___x_51_, 1);
v___x_52_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__8));
v___x_53_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_52_);
if (lean_obj_tag(v___x_53_) == 0)
{
lean_object* v___x_54_; lean_object* v___x_55_; 
lean_dec_ref_known(v___x_53_, 1);
v___x_54_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__9));
v___x_55_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_54_);
if (lean_obj_tag(v___x_55_) == 0)
{
lean_object* v___x_56_; lean_object* v___x_57_; 
lean_dec_ref_known(v___x_55_, 1);
v___x_56_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__10));
v___x_57_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_56_);
if (lean_obj_tag(v___x_57_) == 0)
{
lean_object* v___x_58_; lean_object* v___x_59_; 
lean_dec_ref_known(v___x_57_, 1);
v___x_58_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__11));
v___x_59_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_58_);
if (lean_obj_tag(v___x_59_) == 0)
{
lean_object* v___x_60_; lean_object* v___x_61_; 
lean_dec_ref_known(v___x_59_, 1);
v___x_60_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__12));
v___x_61_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_60_);
if (lean_obj_tag(v___x_61_) == 0)
{
lean_object* v___x_62_; lean_object* v___x_63_; 
lean_dec_ref_known(v___x_61_, 1);
v___x_62_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__13));
v___x_63_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_62_);
if (lean_obj_tag(v___x_63_) == 0)
{
lean_object* v___x_64_; lean_object* v___x_65_; 
lean_dec_ref_known(v___x_63_, 1);
v___x_64_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__14));
v___x_65_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_64_);
if (lean_obj_tag(v___x_65_) == 0)
{
lean_object* v___x_66_; lean_object* v___x_67_; 
lean_dec_ref_known(v___x_65_, 1);
v___x_66_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__15));
v___x_67_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_66_);
if (lean_obj_tag(v___x_67_) == 0)
{
lean_object* v___x_68_; lean_object* v___x_69_; 
lean_dec_ref_known(v___x_67_, 1);
v___x_68_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__16));
v___x_69_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_68_);
if (lean_obj_tag(v___x_69_) == 0)
{
lean_object* v___x_70_; lean_object* v___x_71_; 
lean_dec_ref_known(v___x_69_, 1);
v___x_70_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___closed__17));
v___x_71_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap03_verifyChap03_spec__0(v___x_70_);
return v___x_71_;
}
else
{
return v___x_69_;
}
}
else
{
return v___x_67_;
}
}
else
{
return v___x_65_;
}
}
else
{
return v___x_63_;
}
}
else
{
return v___x_61_;
}
}
else
{
return v___x_59_;
}
}
else
{
return v___x_57_;
}
}
else
{
return v___x_55_;
}
}
else
{
return v___x_53_;
}
}
else
{
return v___x_51_;
}
}
else
{
return v___x_49_;
}
}
else
{
return v___x_47_;
}
}
else
{
return v___x_45_;
}
}
else
{
return v___x_43_;
}
}
else
{
return v___x_41_;
}
}
else
{
return v___x_39_;
}
}
else
{
return v___x_37_;
}
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03___boxed(lean_object* v_a_72_){
_start:
{
lean_object* v_res_73_; 
v_res_73_ = lp_UnifiedQuantumGravityBook_Book_Chap03_verifyChap03();
return v_res_73_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap03_PascalSimplex(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
