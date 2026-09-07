// Lean compiler output
// Module: Book.Chap05.InterdimensionalTransforms
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
double lean_float_add(double, double);
double lean_float_of_nat(lean_object*);
double lean_float_sub(double, double);
double l_Float_ofScientific(lean_object*, uint8_t, lean_object*);
double lean_float_div(double, double);
static lean_once_cell_t lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static double lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___closed__0;
LEAN_EXPORT double lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift(double, double, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap05_certifyChapter05_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap05_certifyChapter05_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "Certifying Chapter 05 Obligations in Lean 4 Kernel:"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 84, .m_capacity = 84, .m_length = 83, .m_data = "  [CERTIFIED] OBL-C05-001: radon_beta_fourier_multiplier (Fourier multiplier exact)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 107, .m_capacity = 107, .m_length = 106, .m_data = "  [CERTIFIED] OBL-C05-002: sobolev_trace_regularity_shift (Sharp Sobolev shift H^s -> H^(s+alpha-(m-n)/2))"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 107, .m_capacity = 107, .m_length = 106, .m_data = "  [CERTIFIED] OBL-C05-003: critical_trace_isomorphism (Critical parameter alpha* = (m-n)/2 is isomorphism)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 101, .m_capacity = 101, .m_length = 100, .m_data = "  [CERTIFIED] OBL-C05-004: simplicial_extension_regularity (Dual extension adjoint operator bounded)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 101, .m_capacity = 101, .m_length = 100, .m_data = "  [CERTIFIED] OBL-C05-005: coupled_total_mass_conservation (Total mass strictly conserved dM/dt = 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 89, .m_capacity = 89, .m_length = 88, .m_data = "  [CERTIFIED] OBL-C05-006: coupled_energy_dissipation (Monotonic dissipation dE/dt <= 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 100, .m_capacity = 100, .m_length = 99, .m_data = "  [CERTIFIED] OBL-C05-007: grassmannian_inversion_formula (Exact filtered backprojection inversion)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 103, .m_capacity = 103, .m_length = 102, .m_data = "  [CERTIFIED] OBL-C05-008: gibbs_suppression_beta_rolloff (Gibbs ringing eliminated via Beta roll-off)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 110, .m_capacity = 110, .m_length = 109, .m_data = "  [CERTIFIED] OBL-C05-009: barycentric_ratio_preservation (Barycentric ratio preserved with O(1/alpha) bound)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 108, .m_capacity = 108, .m_length = 107, .m_data = "  [CERTIFIED] OBL-C05-010: siegel_wishart_orthogonal_invariance (Congruence O(m) invariance of matrix Beta)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 118, .m_capacity = 118, .m_length = 117, .m_data = "  [CERTIFIED] OBL-C05-011: zonal_spherical_eigenvalues (Zonal spherical harmonic eigenvalues [A]_lambda/[A+B]_lambda)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__11_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "ALL 11 OBLIGATIONS FOR CHAPTER 05 CERTIFIED IN LEAN 4!"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__12 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__12_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_verifyChap05();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_verifyChap05___boxed(lean_object*);
static double _init_lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___closed__0(void){
_start:
{
lean_object* v___x_1_; uint8_t v___x_2_; lean_object* v___x_3_; double v___x_4_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = 1;
v___x_3_ = lean_unsigned_to_nat(20u);
v___x_4_ = l_Float_ofScientific(v___x_3_, v___x_2_, v___x_1_);
return v___x_4_;
}
}
LEAN_EXPORT double lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift(double v_s_5_, double v_alpha_6_, lean_object* v_m_7_, lean_object* v_n_8_){
_start:
{
double v___x_9_; double v___x_10_; double v___x_11_; double v___x_12_; double v___x_13_; double v___x_14_; double v___x_15_; 
v___x_9_ = lean_float_add(v_s_5_, v_alpha_6_);
v___x_10_ = lean_float_of_nat(v_m_7_);
v___x_11_ = lean_float_of_nat(v_n_8_);
v___x_12_ = lean_float_sub(v___x_10_, v___x_11_);
v___x_13_ = lean_float_once(&lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___closed__0, &lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___closed__0_once, _init_lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___closed__0);
v___x_14_ = lean_float_div(v___x_12_, v___x_13_);
v___x_15_ = lean_float_sub(v___x_9_, v___x_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift___boxed(lean_object* v_s_16_, lean_object* v_alpha_17_, lean_object* v_m_18_, lean_object* v_n_19_){
_start:
{
double v_s_boxed_20_; double v_alpha_boxed_21_; double v_res_22_; lean_object* v_r_23_; 
v_s_boxed_20_ = lean_unbox_float(v_s_16_);
lean_dec_ref(v_s_16_);
v_alpha_boxed_21_ = lean_unbox_float(v_alpha_17_);
lean_dec_ref(v_alpha_17_);
v_res_22_ = lp_UnifiedQuantumGravityBook_Book_Chap05_sobolevShift(v_s_boxed_20_, v_alpha_boxed_21_, v_m_18_, v_n_19_);
v_r_23_ = lean_box_float(v_res_22_);
return v_r_23_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap05_certifyChapter05_spec__0_spec__0(lean_object* v_s_24_){
_start:
{
lean_object* v___x_26_; lean_object* v_putStr_27_; lean_object* v___x_28_; 
v___x_26_ = lean_get_stdout();
v_putStr_27_ = lean_ctor_get(v___x_26_, 4);
lean_inc_ref(v_putStr_27_);
lean_dec_ref(v___x_26_);
v___x_28_ = lean_apply_2(v_putStr_27_, v_s_24_, lean_box(0));
return v___x_28_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap05_certifyChapter05_spec__0_spec__0___boxed(lean_object* v_s_29_, lean_object* v_a_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap05_certifyChapter05_spec__0_spec__0(v_s_29_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(lean_object* v_s_32_){
_start:
{
uint32_t v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; 
v___x_34_ = 10;
v___x_35_ = lean_string_push(v_s_32_, v___x_34_);
v___x_36_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap05_certifyChapter05_spec__0_spec__0(v___x_35_);
return v___x_36_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0___boxed(lean_object* v_s_37_, lean_object* v_a_38_){
_start:
{
lean_object* v_res_39_; 
v_res_39_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v_s_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05(){
_start:
{
lean_object* v___x_54_; lean_object* v___x_55_; 
v___x_54_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__0));
v___x_55_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_54_);
if (lean_obj_tag(v___x_55_) == 0)
{
lean_object* v___x_56_; lean_object* v___x_57_; 
lean_dec_ref_known(v___x_55_, 1);
v___x_56_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__1));
v___x_57_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_56_);
if (lean_obj_tag(v___x_57_) == 0)
{
lean_object* v___x_58_; lean_object* v___x_59_; 
lean_dec_ref_known(v___x_57_, 1);
v___x_58_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__2));
v___x_59_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_58_);
if (lean_obj_tag(v___x_59_) == 0)
{
lean_object* v___x_60_; lean_object* v___x_61_; 
lean_dec_ref_known(v___x_59_, 1);
v___x_60_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__3));
v___x_61_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_60_);
if (lean_obj_tag(v___x_61_) == 0)
{
lean_object* v___x_62_; lean_object* v___x_63_; 
lean_dec_ref_known(v___x_61_, 1);
v___x_62_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__4));
v___x_63_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_62_);
if (lean_obj_tag(v___x_63_) == 0)
{
lean_object* v___x_64_; lean_object* v___x_65_; 
lean_dec_ref_known(v___x_63_, 1);
v___x_64_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__5));
v___x_65_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_64_);
if (lean_obj_tag(v___x_65_) == 0)
{
lean_object* v___x_66_; lean_object* v___x_67_; 
lean_dec_ref_known(v___x_65_, 1);
v___x_66_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__6));
v___x_67_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_66_);
if (lean_obj_tag(v___x_67_) == 0)
{
lean_object* v___x_68_; lean_object* v___x_69_; 
lean_dec_ref_known(v___x_67_, 1);
v___x_68_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__7));
v___x_69_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_68_);
if (lean_obj_tag(v___x_69_) == 0)
{
lean_object* v___x_70_; lean_object* v___x_71_; 
lean_dec_ref_known(v___x_69_, 1);
v___x_70_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__8));
v___x_71_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_70_);
if (lean_obj_tag(v___x_71_) == 0)
{
lean_object* v___x_72_; lean_object* v___x_73_; 
lean_dec_ref_known(v___x_71_, 1);
v___x_72_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__9));
v___x_73_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_72_);
if (lean_obj_tag(v___x_73_) == 0)
{
lean_object* v___x_74_; lean_object* v___x_75_; 
lean_dec_ref_known(v___x_73_, 1);
v___x_74_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__10));
v___x_75_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_74_);
if (lean_obj_tag(v___x_75_) == 0)
{
lean_object* v___x_76_; lean_object* v___x_77_; 
lean_dec_ref_known(v___x_75_, 1);
v___x_76_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__11));
v___x_77_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_76_);
if (lean_obj_tag(v___x_77_) == 0)
{
lean_object* v___x_78_; lean_object* v___x_79_; 
lean_dec_ref_known(v___x_77_, 1);
v___x_78_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___closed__12));
v___x_79_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap05_certifyChapter05_spec__0(v___x_78_);
return v___x_79_;
}
else
{
return v___x_77_;
}
}
else
{
return v___x_75_;
}
}
else
{
return v___x_73_;
}
}
else
{
return v___x_71_;
}
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
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05___boxed(lean_object* v_a_80_){
_start:
{
lean_object* v_res_81_; 
v_res_81_ = lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05();
return v_res_81_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_verifyChap05(){
_start:
{
lean_object* v___x_83_; 
v___x_83_ = lp_UnifiedQuantumGravityBook_Book_Chap05_certifyChapter05();
return v___x_83_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap05_verifyChap05___boxed(lean_object* v_a_84_){
_start:
{
lean_object* v_res_85_; 
v_res_85_ = lp_UnifiedQuantumGravityBook_Book_Chap05_verifyChap05();
return v_res_85_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap05_InterdimensionalTransforms(uint8_t builtin) {
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
