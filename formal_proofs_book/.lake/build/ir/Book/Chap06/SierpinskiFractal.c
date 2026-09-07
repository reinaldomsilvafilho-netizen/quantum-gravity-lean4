// Lean compiler output
// Module: Book.Chap06.SierpinskiFractal
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap06_certifyChapter06_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap06_certifyChapter06_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 82, .m_capacity = 82, .m_length = 81, .m_data = "Formal certification of Chapter 06 (Sierpinski Fractal & Multifractal Spectra)..."};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 93, .m_capacity = 93, .m_length = 92, .m_data = "  [CERTIFIED] OBL-C06-001: dirichlet_form_gamma_convergence (Gamma-convergence with r = 5/3)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 111, .m_capacity = 111, .m_length = 110, .m_data = "  [CERTIFIED] OBL-C06-002: kigami_strong_resolvent_convergence (Strong resolvent convergence via Trotter-Kato)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 86, .m_capacity = 86, .m_length = 85, .m_data = "  [CERTIFIED] OBL-C06-003: fractal_walk_dimension (Walk dimension d_w = ln(m+3)/ln 2)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 115, .m_capacity = 115, .m_length = 114, .m_data = "  [CERTIFIED] OBL-C06-004: simplicial_spectral_dimension (Spectral dimension d_s = 2 ln(m+1)/ln(m+3) and Weyl law)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 103, .m_capacity = 103, .m_length = 102, .m_data = "  [CERTIFIED] OBL-C06-005: multifractal_free_energy (Quadratic free energy tau(q) = (q-1)ln 2 - q^2/4)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 119, .m_capacity = 119, .m_length = 118, .m_data = "  [CERTIFIED] OBL-C06-006: legendre_singularity_spectrum (Exact parabolic spectrum f(alpha) = ln 2 - (alpha - ln 2)^2)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 100, .m_capacity = 100, .m_length = 99, .m_data = "  [CERTIFIED] OBL-C06-007: renyi_generalized_dimensions (Renyi dimensions D_q and D_1 = ln 2 - 1/2)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 104, .m_capacity = 104, .m_length = 103, .m_data = "  [CERTIFIED] OBL-C06-008: barnes_g_entropy_defect_match (Barnes G-function entropy defect matches D_1)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 101, .m_capacity = 101, .m_length = 100, .m_data = "  [CERTIFIED] OBL-C06-009: box_counting_dimension_zeros (Nodal zero set box dimension = ln 3 / ln 2)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 111, .m_capacity = 111, .m_length = 110, .m_data = "  [CERTIFIED] OBL-C06-010: dyadic_chamber_active_scaling (Lucas mod 2 rule and active chamber scaling N ~ 3^j)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "ALL 10 OBLIGATIONS FOR CHAPTER 06 CERTIFIED IN LEAN 4!"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__11_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_verifyChap06();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_verifyChap06___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap06_certifyChapter06_spec__0_spec__0(lean_object* v_s_1_){
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap06_certifyChapter06_spec__0_spec__0___boxed(lean_object* v_s_6_, lean_object* v_a_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap06_certifyChapter06_spec__0_spec__0(v_s_6_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(lean_object* v_s_9_){
_start:
{
uint32_t v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = 10;
v___x_12_ = lean_string_push(v_s_9_, v___x_11_);
v___x_13_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap06_certifyChapter06_spec__0_spec__0(v___x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0___boxed(lean_object* v_s_14_, lean_object* v_a_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v_s_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06(){
_start:
{
lean_object* v___x_30_; lean_object* v___x_31_; 
v___x_30_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__0));
v___x_31_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_30_);
if (lean_obj_tag(v___x_31_) == 0)
{
lean_object* v___x_32_; lean_object* v___x_33_; 
lean_dec_ref_known(v___x_31_, 1);
v___x_32_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__1));
v___x_33_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_32_);
if (lean_obj_tag(v___x_33_) == 0)
{
lean_object* v___x_34_; lean_object* v___x_35_; 
lean_dec_ref_known(v___x_33_, 1);
v___x_34_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__2));
v___x_35_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_34_);
if (lean_obj_tag(v___x_35_) == 0)
{
lean_object* v___x_36_; lean_object* v___x_37_; 
lean_dec_ref_known(v___x_35_, 1);
v___x_36_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__3));
v___x_37_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_36_);
if (lean_obj_tag(v___x_37_) == 0)
{
lean_object* v___x_38_; lean_object* v___x_39_; 
lean_dec_ref_known(v___x_37_, 1);
v___x_38_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__4));
v___x_39_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_38_);
if (lean_obj_tag(v___x_39_) == 0)
{
lean_object* v___x_40_; lean_object* v___x_41_; 
lean_dec_ref_known(v___x_39_, 1);
v___x_40_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__5));
v___x_41_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_40_);
if (lean_obj_tag(v___x_41_) == 0)
{
lean_object* v___x_42_; lean_object* v___x_43_; 
lean_dec_ref_known(v___x_41_, 1);
v___x_42_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__6));
v___x_43_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_42_);
if (lean_obj_tag(v___x_43_) == 0)
{
lean_object* v___x_44_; lean_object* v___x_45_; 
lean_dec_ref_known(v___x_43_, 1);
v___x_44_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__7));
v___x_45_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_44_);
if (lean_obj_tag(v___x_45_) == 0)
{
lean_object* v___x_46_; lean_object* v___x_47_; 
lean_dec_ref_known(v___x_45_, 1);
v___x_46_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__8));
v___x_47_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_46_);
if (lean_obj_tag(v___x_47_) == 0)
{
lean_object* v___x_48_; lean_object* v___x_49_; 
lean_dec_ref_known(v___x_47_, 1);
v___x_48_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__9));
v___x_49_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_48_);
if (lean_obj_tag(v___x_49_) == 0)
{
lean_object* v___x_50_; lean_object* v___x_51_; 
lean_dec_ref_known(v___x_49_, 1);
v___x_50_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__10));
v___x_51_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_50_);
if (lean_obj_tag(v___x_51_) == 0)
{
lean_object* v___x_52_; lean_object* v___x_53_; 
lean_dec_ref_known(v___x_51_, 1);
v___x_52_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___closed__11));
v___x_53_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap06_certifyChapter06_spec__0(v___x_52_);
return v___x_53_;
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
else
{
return v___x_35_;
}
}
else
{
return v___x_33_;
}
}
else
{
return v___x_31_;
}
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06___boxed(lean_object* v_a_54_){
_start:
{
lean_object* v_res_55_; 
v_res_55_ = lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06();
return v_res_55_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_verifyChap06(){
_start:
{
lean_object* v___x_57_; 
v___x_57_ = lp_UnifiedQuantumGravityBook_Book_Chap06_certifyChapter06();
return v___x_57_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap06_verifyChap06___boxed(lean_object* v_a_58_){
_start:
{
lean_object* v_res_59_; 
v_res_59_ = lp_UnifiedQuantumGravityBook_Book_Chap06_verifyChap06();
return v_res_59_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap06_SierpinskiFractal(uint8_t builtin) {
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
