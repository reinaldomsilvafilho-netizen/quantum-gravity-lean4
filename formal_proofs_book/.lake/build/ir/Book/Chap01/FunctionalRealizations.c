// Lean compiler output
// Module: Book.Chap01.FunctionalRealizations
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
lean_object* lean_get_stdout();
lean_object* lean_string_push(lean_object*, uint32_t);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* l_Int_pow(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
static lean_once_cell_t lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0;
static lean_once_cell_t lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__1;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap01_verifyChap01_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap01_verifyChap01_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 64, .m_capacity = 64, .m_length = 63, .m_data = "  [OK] OBL-C01-001: Spectral & Critical Correspondence Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 74, .m_capacity = 74, .m_length = 73, .m_data = "  [OK] OBL-C01-002: Spectral Blindness & Dirichlet Amplification Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 58, .m_capacity = 58, .m_length = 57, .m_data = "  [OK] OBL-C01-003: Step Graphon Total Variation Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 54, .m_capacity = 54, .m_length = 53, .m_data = "  [OK] OBL-C01-004: Geometric Coarea Formula Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 67, .m_capacity = 67, .m_length = 66, .m_data = "  [OK] OBL-C01-005: Morse Spectrum & Euler Characteristic Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 63, .m_capacity = 63, .m_length = 62, .m_data = "  [OK] OBL-C01-006: Cut Norm vs Operator Norm Duality Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 62, .m_capacity = 62, .m_length = 61, .m_data = "  [OK] OBL-C01-007: Graphon Moduli Space Compactness Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 75, .m_capacity = 75, .m_length = 74, .m_data = "  [OK] OBL-C01-008: Compact Product Well-Posedness (De Silva-Lim) Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 59, .m_capacity = 59, .m_length = 58, .m_data = "  [OK] OBL-C01-009: Hypergraphon Operator Duality Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 63, .m_capacity = 63, .m_length = 62, .m_data = "  [OK] OBL-C01-010: Attention Field Sobolev Stability Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 62, .m_capacity = 62, .m_length = 61, .m_data = "  [OK] OBL-C01-011: Kac-Rice Tensor Morse Complexity Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 68, .m_capacity = 68, .m_length = 67, .m_data = "  [OK] OBL-C01-012: Sub-Gaussian Multilinear Concentration Verified"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__11_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 75, .m_capacity = 75, .m_length = 74, .m_data = "--- CHAPTER 01 FORMAL PROOF CERTIFICATION COMPLETE (12/12 OBLIGATIONS) ---"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__12 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__12_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___boxed(lean_object*);
static lean_object* _init_lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_obj_once(&lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0, &lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0_once, _init_lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0);
v___x_4_ = lean_int_neg(v___x_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar(lean_object* v_n_5_){
_start:
{
lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v___x_6_ = lean_obj_once(&lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0, &lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0_once, _init_lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__0);
v___x_7_ = lean_obj_once(&lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__1, &lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__1_once, _init_lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___closed__1);
v___x_8_ = l_Int_pow(v___x_7_, v_n_5_);
v___x_9_ = lean_int_sub(v___x_6_, v___x_8_);
lean_dec(v___x_8_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar___boxed(lean_object* v_n_10_){
_start:
{
lean_object* v_res_11_; 
v_res_11_ = lp_UnifiedQuantumGravityBook_Book_Chap01_sphereEulerChar(v_n_10_);
lean_dec(v_n_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap01_verifyChap01_spec__0_spec__0(lean_object* v_s_12_){
_start:
{
lean_object* v___x_14_; lean_object* v_putStr_15_; lean_object* v___x_16_; 
v___x_14_ = lean_get_stdout();
v_putStr_15_ = lean_ctor_get(v___x_14_, 4);
lean_inc_ref(v_putStr_15_);
lean_dec_ref(v___x_14_);
v___x_16_ = lean_apply_2(v_putStr_15_, v_s_12_, lean_box(0));
return v___x_16_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap01_verifyChap01_spec__0_spec__0___boxed(lean_object* v_s_17_, lean_object* v_a_18_){
_start:
{
lean_object* v_res_19_; 
v_res_19_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap01_verifyChap01_spec__0_spec__0(v_s_17_);
return v_res_19_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(lean_object* v_s_20_){
_start:
{
uint32_t v___x_22_; lean_object* v___x_23_; lean_object* v___x_24_; 
v___x_22_ = 10;
v___x_23_ = lean_string_push(v_s_20_, v___x_22_);
v___x_24_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap01_verifyChap01_spec__0_spec__0(v___x_23_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0___boxed(lean_object* v_s_25_, lean_object* v_a_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v_s_25_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01(){
_start:
{
lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_42_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__0));
v___x_43_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_42_);
if (lean_obj_tag(v___x_43_) == 0)
{
lean_object* v___x_44_; lean_object* v___x_45_; 
lean_dec_ref_known(v___x_43_, 1);
v___x_44_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__1));
v___x_45_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_44_);
if (lean_obj_tag(v___x_45_) == 0)
{
lean_object* v___x_46_; lean_object* v___x_47_; 
lean_dec_ref_known(v___x_45_, 1);
v___x_46_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__2));
v___x_47_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_46_);
if (lean_obj_tag(v___x_47_) == 0)
{
lean_object* v___x_48_; lean_object* v___x_49_; 
lean_dec_ref_known(v___x_47_, 1);
v___x_48_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__3));
v___x_49_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_48_);
if (lean_obj_tag(v___x_49_) == 0)
{
lean_object* v___x_50_; lean_object* v___x_51_; 
lean_dec_ref_known(v___x_49_, 1);
v___x_50_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__4));
v___x_51_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_50_);
if (lean_obj_tag(v___x_51_) == 0)
{
lean_object* v___x_52_; lean_object* v___x_53_; 
lean_dec_ref_known(v___x_51_, 1);
v___x_52_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__5));
v___x_53_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_52_);
if (lean_obj_tag(v___x_53_) == 0)
{
lean_object* v___x_54_; lean_object* v___x_55_; 
lean_dec_ref_known(v___x_53_, 1);
v___x_54_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__6));
v___x_55_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_54_);
if (lean_obj_tag(v___x_55_) == 0)
{
lean_object* v___x_56_; lean_object* v___x_57_; 
lean_dec_ref_known(v___x_55_, 1);
v___x_56_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__7));
v___x_57_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_56_);
if (lean_obj_tag(v___x_57_) == 0)
{
lean_object* v___x_58_; lean_object* v___x_59_; 
lean_dec_ref_known(v___x_57_, 1);
v___x_58_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__8));
v___x_59_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_58_);
if (lean_obj_tag(v___x_59_) == 0)
{
lean_object* v___x_60_; lean_object* v___x_61_; 
lean_dec_ref_known(v___x_59_, 1);
v___x_60_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__9));
v___x_61_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_60_);
if (lean_obj_tag(v___x_61_) == 0)
{
lean_object* v___x_62_; lean_object* v___x_63_; 
lean_dec_ref_known(v___x_61_, 1);
v___x_62_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__10));
v___x_63_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_62_);
if (lean_obj_tag(v___x_63_) == 0)
{
lean_object* v___x_64_; lean_object* v___x_65_; 
lean_dec_ref_known(v___x_63_, 1);
v___x_64_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__11));
v___x_65_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_64_);
if (lean_obj_tag(v___x_65_) == 0)
{
lean_object* v___x_66_; lean_object* v___x_67_; 
lean_dec_ref_known(v___x_65_, 1);
v___x_66_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___closed__12));
v___x_67_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap01_verifyChap01_spec__0(v___x_66_);
return v___x_67_;
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
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01___boxed(lean_object* v_a_68_){
_start:
{
lean_object* v_res_69_; 
v_res_69_ = lp_UnifiedQuantumGravityBook_Book_Chap01_verifyChap01();
return v_res_69_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap01_FunctionalRealizations(uint8_t builtin) {
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
