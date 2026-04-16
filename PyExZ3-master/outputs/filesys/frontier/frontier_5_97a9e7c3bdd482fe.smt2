(set-logic ALL)
; Constraint ID: 97a9e7c3bdd482fe
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59692)) (False)
(assert (not (= x 59692)))

; Query: ((== x 59693)) (False)
(assert (not (not (= x 59693))))

(check-sat)
(get-model)
