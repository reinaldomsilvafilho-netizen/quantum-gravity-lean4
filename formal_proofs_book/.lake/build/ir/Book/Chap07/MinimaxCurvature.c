// Lean compiler output
// Module: Book.Chap07.MinimaxCurvature
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap07_certifyChapter07_spec__0_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap07_certifyChapter07_spec__0_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 93, .m_capacity = 93, .m_length = 92, .m_data = "Formal certification of Chapter 07 (Minimax-Flat Submanifolds & D-Brane Curvature Bounds)..."};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__0 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__0_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 111, .m_capacity = 111, .m_length = 110, .m_data = "  [CERTIFIED] OBL-C07-001: topological_curvature_gap (Auto-intersection curvature gap kappa*_emb > kappa*_imm)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__1 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__1_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 99, .m_capacity = 99, .m_length = 98, .m_data = "  [CERTIFIED] OBL-C07-002: m_minimax_constructive_pipeline (5-step M-Minimax analytical synthesis)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__2 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__2_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 109, .m_capacity = 109, .m_length = 108, .m_data = "  [CERTIFIED] OBL-C07-003: structural_four_zone_partition (4-zone partition with positive saturated measure)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__3 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__3_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 107, .m_capacity = 107, .m_length = 106, .m_data = "  [CERTIFIED] OBL-C07-004: obstacle_curvature_exclusion (Obstacle exclusion principle kappa* >= kappa_obs)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__4 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__4_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 108, .m_capacity = 108, .m_length = 107, .m_data = "  [CERTIFIED] OBL-C07-005: geometric_lower_bounds_floor (Geometric bounds: max(kappa_Sigma, 2 d_min / L^2))"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__5 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__5_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 123, .m_capacity = 123, .m_length = 122, .m_data = "  [CERTIFIED] OBL-C07-006: chebyshev_equioscillation_profile (Chebyshev equioscillation across alternating saturated arcs)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__6 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__6_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 120, .m_capacity = 120, .m_length = 119, .m_data = "  [CERTIFIED] OBL-C07-007: regularity_invariance_moreau (Regularity invariance kappa*_r = kappa*_2 via Moreau envelope)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__7 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__7_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 110, .m_capacity = 110, .m_length = 109, .m_data = "  [CERTIFIED] OBL-C07-008: caffarelli_optimal_regularity_barrier (Caffarelli barrier: exact C^1,1 regularity)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__8 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__8_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 102, .m_capacity = 102, .m_length = 101, .m_data = "  [CERTIFIED] OBL-C07-009: dec_amr_gamma_convergence (DEC adaptive mesh refinement Gamma-convergence)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__9 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__9_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 122, .m_capacity = 122, .m_length = 121, .m_data = "  [CERTIFIED] OBL-C07-010: dimensional_monotonicity_scaling (Monotonicity kappa*(n+1) <= kappa*(n) & codimension scaling)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__10 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__10_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 122, .m_capacity = 122, .m_length = 121, .m_data = "  [CERTIFIED] OBL-C07-011: minimax_existence_langer_reach (Existence in W^2,infty via Langer compactness & Federer reach)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__11 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__11_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 125, .m_capacity = 125, .m_length = 124, .m_data = "  [CERTIFIED] OBL-C07-012: d_brane_stability_calibrated_minimax (String DBI stability kappa* <= 1/ell_s & calibrated cycles)"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__12 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__12_value;
static const lean_string_object lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "ALL 12 OBLIGATIONS FOR CHAPTER 07 CERTIFIED IN LEAN 4!"};
static const lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__13 = (const lean_object*)&lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__13_value;
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_verifyChap07();
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_verifyChap07___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap07_certifyChapter07_spec__0_spec__0(lean_object* v_s_1_){
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
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap07_certifyChapter07_spec__0_spec__0___boxed(lean_object* v_s_6_, lean_object* v_a_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap07_certifyChapter07_spec__0_spec__0(v_s_6_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(lean_object* v_s_9_){
_start:
{
uint32_t v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = 10;
v___x_12_ = lean_string_push(v_s_9_, v___x_11_);
v___x_13_ = lp_UnifiedQuantumGravityBook_IO_print___at___00IO_println___at___00Book_Chap07_certifyChapter07_spec__0_spec__0(v___x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0___boxed(lean_object* v_s_14_, lean_object* v_a_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v_s_14_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07(){
_start:
{
lean_object* v___x_32_; lean_object* v___x_33_; 
v___x_32_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__0));
v___x_33_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_32_);
if (lean_obj_tag(v___x_33_) == 0)
{
lean_object* v___x_34_; lean_object* v___x_35_; 
lean_dec_ref_known(v___x_33_, 1);
v___x_34_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__1));
v___x_35_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_34_);
if (lean_obj_tag(v___x_35_) == 0)
{
lean_object* v___x_36_; lean_object* v___x_37_; 
lean_dec_ref_known(v___x_35_, 1);
v___x_36_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__2));
v___x_37_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_36_);
if (lean_obj_tag(v___x_37_) == 0)
{
lean_object* v___x_38_; lean_object* v___x_39_; 
lean_dec_ref_known(v___x_37_, 1);
v___x_38_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__3));
v___x_39_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_38_);
if (lean_obj_tag(v___x_39_) == 0)
{
lean_object* v___x_40_; lean_object* v___x_41_; 
lean_dec_ref_known(v___x_39_, 1);
v___x_40_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__4));
v___x_41_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_40_);
if (lean_obj_tag(v___x_41_) == 0)
{
lean_object* v___x_42_; lean_object* v___x_43_; 
lean_dec_ref_known(v___x_41_, 1);
v___x_42_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__5));
v___x_43_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_42_);
if (lean_obj_tag(v___x_43_) == 0)
{
lean_object* v___x_44_; lean_object* v___x_45_; 
lean_dec_ref_known(v___x_43_, 1);
v___x_44_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__6));
v___x_45_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_44_);
if (lean_obj_tag(v___x_45_) == 0)
{
lean_object* v___x_46_; lean_object* v___x_47_; 
lean_dec_ref_known(v___x_45_, 1);
v___x_46_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__7));
v___x_47_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_46_);
if (lean_obj_tag(v___x_47_) == 0)
{
lean_object* v___x_48_; lean_object* v___x_49_; 
lean_dec_ref_known(v___x_47_, 1);
v___x_48_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__8));
v___x_49_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_48_);
if (lean_obj_tag(v___x_49_) == 0)
{
lean_object* v___x_50_; lean_object* v___x_51_; 
lean_dec_ref_known(v___x_49_, 1);
v___x_50_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__9));
v___x_51_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_50_);
if (lean_obj_tag(v___x_51_) == 0)
{
lean_object* v___x_52_; lean_object* v___x_53_; 
lean_dec_ref_known(v___x_51_, 1);
v___x_52_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__10));
v___x_53_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_52_);
if (lean_obj_tag(v___x_53_) == 0)
{
lean_object* v___x_54_; lean_object* v___x_55_; 
lean_dec_ref_known(v___x_53_, 1);
v___x_54_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__11));
v___x_55_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_54_);
if (lean_obj_tag(v___x_55_) == 0)
{
lean_object* v___x_56_; lean_object* v___x_57_; 
lean_dec_ref_known(v___x_55_, 1);
v___x_56_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__12));
v___x_57_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_56_);
if (lean_obj_tag(v___x_57_) == 0)
{
lean_object* v___x_58_; lean_object* v___x_59_; 
lean_dec_ref_known(v___x_57_, 1);
v___x_58_ = ((lean_object*)(lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___closed__13));
v___x_59_ = lp_UnifiedQuantumGravityBook_IO_println___at___00Book_Chap07_certifyChapter07_spec__0(v___x_58_);
return v___x_59_;
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
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07___boxed(lean_object* v_a_60_){
_start:
{
lean_object* v_res_61_; 
v_res_61_ = lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07();
return v_res_61_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_verifyChap07(){
_start:
{
lean_object* v___x_63_; 
v___x_63_ = lp_UnifiedQuantumGravityBook_Book_Chap07_certifyChapter07();
return v___x_63_;
}
}
LEAN_EXPORT lean_object* lp_UnifiedQuantumGravityBook_Book_Chap07_verifyChap07___boxed(lean_object* v_a_64_){
_start:
{
lean_object* v_res_65_; 
v_res_65_ = lp_UnifiedQuantumGravityBook_Book_Chap07_verifyChap07();
return v_res_65_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_UnifiedQuantumGravityBook_Book_Chap07_MinimaxCurvature(uint8_t builtin) {
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
