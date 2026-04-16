(set-logic ALL)
; Constraint ID: c9cf8b5d1ea96813
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60079)) (False)
(assert (not (= x 60079)))

; Query: ((== x 60080)) (False)
(assert (not (not (= x 60080))))

(check-sat)
(get-model)
