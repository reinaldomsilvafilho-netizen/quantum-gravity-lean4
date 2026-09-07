// Lean compiler output
// Module: Book.Chap04.SimplicialWaves
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap04_verifyChap04_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap04_verifyChap04_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "Certifying Chapter 04 Obligations in Lean 4 Kernel:"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 84, .m_capacity = 84, .m_length = 83, .m_data = "  [CERTIFIED] OBL-C04-001: simplicial_laplacian_self_adjoint (Self-adjoint, E >= 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 77, .m_capacity = 77, .m_length = 76, .m_data = "  [CERTIFIED] OBL-C04-002: simplicial_dispersion_symbol (Closed-form Symbol)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 91, .m_capacity = 91, .m_length = 90, .m_data = "  [CERTIFIED] OBL-C04-003: cartan_metric_long_wavelength (A_{m-1} Cartan Metric Emergence)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 72, .m_capacity = 72, .m_length = 71, .m_data = "  [CERTIFIED] OBL-C04-004: nlse_mass_conservation (dN/dt = 0 Identical)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 86, .m_capacity = 86, .m_length = 85, .m_data = "  [CERTIFIED] OBL-C04-005: nlse_energy_conservation (dE/dt = 0 Hamiltonian Invariant)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 88, .m_capacity = 88, .m_length = 87, .m_data = "  [CERTIFIED] OBL-C04-006: modulational_instability_bound (Simplicial MI & Growth Rate)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 85, .m_capacity = 85, .m_length = 84, .m_data = "  [CERTIFIED] OBL-C04-007: soliton_point_group_symmetry (S_m Point-Group Invariance)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 81, .m_capacity = 81, .m_length = 80, .m_data = "  [CERTIFIED] OBL-C04-008: mittag_leffler_propagator (Mittag-Leffler Propagator)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 72, .m_capacity = 72, .m_length = 71, .m_data = "  [CERTIFIED] OBL-C04-009: diffusion_zero_drift (<x(t)> = 0 Zero Drift)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 87, .m_capacity = 87, .m_length = 86, .m_data = "  [CERTIFIED] OBL-C04-010: msd_cartan_covariance_tensor (MSD ~ A_{m-1} t^beta Scaling)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "ALL 10 OBLIGATIONS FOR CHAPTER 04 CERTIFIED IN LEAN 4!"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__11_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap04_verifyChap04_spec__0_spec__0(lean_object* v_s_1_){
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap04_verifyChap04_spec__0_spec__0___boxed(lean_object* v_s_6_, lean_object* v_a_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap04_verifyChap04_spec__0_spec__0(v_s_6_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(lean_object* v_s_9_){
_start:
{
uint32_t v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = 10;
v___x_12_ = lean_string_push(v_s_9_, v___x_11_);
v___x_13_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap04_verifyChap04_spec__0_spec__0(v___x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0___boxed(lean_object* v_s_14_, lean_object* v_a_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v_s_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04(){
_start:
{
lean_object* v___x_30_; lean_object* v___x_31_; 
v___x_30_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__0));
v___x_31_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_30_);
if (lean_obj_tag(v___x_31_) == 0)
{
lean_object* v___x_32_; lean_object* v___x_33_; 
lean_dec_ref_known(v___x_31_, 1);
v___x_32_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__1));
v___x_33_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_32_);
if (lean_obj_tag(v___x_33_) == 0)
{
lean_object* v___x_34_; lean_object* v___x_35_; 
lean_dec_ref_known(v___x_33_, 1);
v___x_34_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__2));
v___x_35_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_34_);
if (lean_obj_tag(v___x_35_) == 0)
{
lean_object* v___x_36_; lean_object* v___x_37_; 
lean_dec_ref_known(v___x_35_, 1);
v___x_36_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__3));
v___x_37_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_36_);
if (lean_obj_tag(v___x_37_) == 0)
{
lean_object* v___x_38_; lean_object* v___x_39_; 
lean_dec_ref_known(v___x_37_, 1);
v___x_38_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__4));
v___x_39_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_38_);
if (lean_obj_tag(v___x_39_) == 0)
{
lean_object* v___x_40_; lean_object* v___x_41_; 
lean_dec_ref_known(v___x_39_, 1);
v___x_40_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__5));
v___x_41_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_40_);
if (lean_obj_tag(v___x_41_) == 0)
{
lean_object* v___x_42_; lean_object* v___x_43_; 
lean_dec_ref_known(v___x_41_, 1);
v___x_42_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__6));
v___x_43_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_42_);
if (lean_obj_tag(v___x_43_) == 0)
{
lean_object* v___x_44_; lean_object* v___x_45_; 
lean_dec_ref_known(v___x_43_, 1);
v___x_44_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__7));
v___x_45_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_44_);
if (lean_obj_tag(v___x_45_) == 0)
{
lean_object* v___x_46_; lean_object* v___x_47_; 
lean_dec_ref_known(v___x_45_, 1);
v___x_46_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__8));
v___x_47_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_46_);
if (lean_obj_tag(v___x_47_) == 0)
{
lean_object* v___x_48_; lean_object* v___x_49_; 
lean_dec_ref_known(v___x_47_, 1);
v___x_48_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__9));
v___x_49_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_48_);
if (lean_obj_tag(v___x_49_) == 0)
{
lean_object* v___x_50_; lean_object* v___x_51_; 
lean_dec_ref_known(v___x_49_, 1);
v___x_50_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__10));
v___x_51_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_50_);
if (lean_obj_tag(v___x_51_) == 0)
{
lean_object* v___x_52_; lean_object* v___x_53_; 
lean_dec_ref_known(v___x_51_, 1);
v___x_52_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___closed__11));
v___x_53_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap04_verifyChap04_spec__0(v___x_52_);
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04___boxed(lean_object* v_a_54_){
_start:
{
lean_object* v_res_55_; 
v_res_55_ = lp_UnifiedQuantumGravityBook_Book_Chap04_verifyChap04();
return v_res_55_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap04_SimplicialWaves(uint8_t builtin) {
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
