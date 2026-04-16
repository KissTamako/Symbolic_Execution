(set-logic ALL)
; Constraint ID: e689edb1b7b2ce69
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59686)) (False)
(assert (not (= x 59686)))

; Query: ((== x 59687)) (False)
(assert (not (not (= x 59687))))

(check-sat)
(get-model)
