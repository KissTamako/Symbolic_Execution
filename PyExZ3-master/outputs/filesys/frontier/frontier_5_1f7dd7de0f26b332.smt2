(set-logic ALL)
; Constraint ID: 1f7dd7de0f26b332
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60067)) (False)
(assert (not (= x 60067)))

; Query: ((== x 60068)) (False)
(assert (not (not (= x 60068))))

(check-sat)
(get-model)
