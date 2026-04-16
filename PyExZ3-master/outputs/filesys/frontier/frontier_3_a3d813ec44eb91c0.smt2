(set-logic ALL)
; Frontier Constraint ID: a3d813ec44eb91c0
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1690)) (False)
(assert (not (= x 1690)))

; Query: ((== x 1691)) (False)
(assert (not (not (= x 1691))))

(check-sat)
(get-model)
