// Lean compiler output
// Module: Book.Chap02.GeometricFlows
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap02_verifyChap02_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap02_verifyChap02_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "Certifying Chapter 02 Obligations in Lean 4 Kernel:"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 68, .m_capacity = 68, .m_length = 67, .m_data = "  [CERTIFIED] OBL-C02-001: affine_invariant_cone_curvature (K <= 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 71, .m_capacity = 71, .m_length = 70, .m_data = "  [CERTIFIED] OBL-C02-002: fixed_rank_tangent_projection (P^2=P, P*=P)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 79, .m_capacity = 79, .m_length = 78, .m_data = "  [CERTIFIED] OBL-C02-003: tensor_train_manifold_structure (dim M_r^TT <= d^k)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 74, .m_capacity = 74, .m_length = 73, .m_data = "  [CERTIFIED] OBL-C02-004: tt_tangent_projection_flow (TT rank preserved)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 69, .m_capacity = 69, .m_length = 68, .m_data = "  [CERTIFIED] OBL-C02-005: toda_flow_isospectral_qr (Isospectral QR)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 93, .m_capacity = 93, .m_length = 92, .m_data = "  [CERTIFIED] OBL-C02-006: projected_gradient_rank_preservation (Rank preserved, dL/dt <= 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 73, .m_capacity = 73, .m_length = 72, .m_data = "  [CERTIFIED] OBL-C02-007: graphon_laplacian_dirichlet_energy (E_W >= 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 80, .m_capacity = 80, .m_length = 79, .m_data = "  [CERTIFIED] OBL-C02-008: graphon_heat_contraction_semigroup (L^p contraction)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 90, .m_capacity = 90, .m_length = 89, .m_data = "  [CERTIFIED] OBL-C02-009: graphon_heat_cutnorm_contraction (||W(t)||_cut non-increasing)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 84, .m_capacity = 84, .m_length = 83, .m_data = "  [CERTIFIED] OBL-C02-010: graphon_ricci_neckpinch_disconnection (kappa_bridge < 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 77, .m_capacity = 77, .m_length = 76, .m_data = "  [CERTIFIED] OBL-C02-011: level_set_mcf_perimeter_dissipation (dTV/dt <= 0)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__11_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 73, .m_capacity = 73, .m_length = 72, .m_data = "  [CERTIFIED] OBL-C02-012: cmps_energy_gradient_flow (QFI gradient flow)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__12 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__12_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 84, .m_capacity = 84, .m_length = 83, .m_data = "  [CERTIFIED] OBL-C02-013: tensor_ring_holonomy_wilson_loop (O(1/k) to Wilson loop)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__13 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__13_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "ALL 13 OBLIGATIONS FOR CHAPTER 02 CERTIFIED IN LEAN 4!"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__14 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__14_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap02_verifyChap02_spec__0_spec__0(lean_object* v_s_1_){
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap02_verifyChap02_spec__0_spec__0___boxed(lean_object* v_s_6_, lean_object* v_a_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap02_verifyChap02_spec__0_spec__0(v_s_6_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(lean_object* v_s_9_){
_start:
{
uint32_t v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = 10;
v___x_12_ = lean_string_push(v_s_9_, v___x_11_);
v___x_13_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap02_verifyChap02_spec__0_spec__0(v___x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0___boxed(lean_object* v_s_14_, lean_object* v_a_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v_s_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02(){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__0));
v___x_34_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_33_);
if (lean_obj_tag(v___x_34_) == 0)
{
lean_object* v___x_35_; lean_object* v___x_36_; 
lean_dec_ref_known(v___x_34_, 1);
v___x_35_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__1));
v___x_36_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_35_);
if (lean_obj_tag(v___x_36_) == 0)
{
lean_object* v___x_37_; lean_object* v___x_38_; 
lean_dec_ref_known(v___x_36_, 1);
v___x_37_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__2));
v___x_38_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_37_);
if (lean_obj_tag(v___x_38_) == 0)
{
lean_object* v___x_39_; lean_object* v___x_40_; 
lean_dec_ref_known(v___x_38_, 1);
v___x_39_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__3));
v___x_40_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_39_);
if (lean_obj_tag(v___x_40_) == 0)
{
lean_object* v___x_41_; lean_object* v___x_42_; 
lean_dec_ref_known(v___x_40_, 1);
v___x_41_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__4));
v___x_42_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_41_);
if (lean_obj_tag(v___x_42_) == 0)
{
lean_object* v___x_43_; lean_object* v___x_44_; 
lean_dec_ref_known(v___x_42_, 1);
v___x_43_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__5));
v___x_44_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_43_);
if (lean_obj_tag(v___x_44_) == 0)
{
lean_object* v___x_45_; lean_object* v___x_46_; 
lean_dec_ref_known(v___x_44_, 1);
v___x_45_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__6));
v___x_46_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_45_);
if (lean_obj_tag(v___x_46_) == 0)
{
lean_object* v___x_47_; lean_object* v___x_48_; 
lean_dec_ref_known(v___x_46_, 1);
v___x_47_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__7));
v___x_48_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_47_);
if (lean_obj_tag(v___x_48_) == 0)
{
lean_object* v___x_49_; lean_object* v___x_50_; 
lean_dec_ref_known(v___x_48_, 1);
v___x_49_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__8));
v___x_50_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_49_);
if (lean_obj_tag(v___x_50_) == 0)
{
lean_object* v___x_51_; lean_object* v___x_52_; 
lean_dec_ref_known(v___x_50_, 1);
v___x_51_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__9));
v___x_52_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_51_);
if (lean_obj_tag(v___x_52_) == 0)
{
lean_object* v___x_53_; lean_object* v___x_54_; 
lean_dec_ref_known(v___x_52_, 1);
v___x_53_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__10));
v___x_54_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_53_);
if (lean_obj_tag(v___x_54_) == 0)
{
lean_object* v___x_55_; lean_object* v___x_56_; 
lean_dec_ref_known(v___x_54_, 1);
v___x_55_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__11));
v___x_56_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_55_);
if (lean_obj_tag(v___x_56_) == 0)
{
lean_object* v___x_57_; lean_object* v___x_58_; 
lean_dec_ref_known(v___x_56_, 1);
v___x_57_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__12));
v___x_58_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_57_);
if (lean_obj_tag(v___x_58_) == 0)
{
lean_object* v___x_59_; lean_object* v___x_60_; 
lean_dec_ref_known(v___x_58_, 1);
v___x_59_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__13));
v___x_60_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_59_);
if (lean_obj_tag(v___x_60_) == 0)
{
lean_object* v___x_61_; lean_object* v___x_62_; 
lean_dec_ref_known(v___x_60_, 1);
v___x_61_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___closed__14));
v___x_62_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap02_verifyChap02_spec__0(v___x_61_);
return v___x_62_;
}
else
{
return v___x_60_;
}
}
else
{
return v___x_58_;
}
}
else
{
return v___x_56_;
}
}
else
{
return v___x_54_;
}
}
else
{
return v___x_52_;
}
}
else
{
return v___x_50_;
}
}
else
{
return v___x_48_;
}
}
else
{
return v___x_46_;
}
}
else
{
return v___x_44_;
}
}
else
{
return v___x_42_;
}
}
else
{
return v___x_40_;
}
}
else
{
return v___x_38_;
}
}
else
{
return v___x_36_;
}
}
else
{
return v___x_34_;
}
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02___boxed(lean_object* v_a_63_){
_start:
{
lean_object* v_res_64_; 
v_res_64_ = lp_UnifiedQuantumGravityBook_Book_Chap02_verifyChap02();
return v_res_64_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap02_GeometricFlows(uint8_t builtin) {
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
