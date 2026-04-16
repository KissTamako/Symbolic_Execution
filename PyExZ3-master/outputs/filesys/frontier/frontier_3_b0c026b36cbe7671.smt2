(set-logic ALL)
; Constraint ID: b0c026b36cbe7671
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59989)) (False)
(assert (not (= x 59989)))

; Query: ((== x 59990)) (False)
(assert (not (not (= x 59990))))

(check-sat)
(get-model)
