(set-logic ALL)
; Constraint ID: 23328992547bc133
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59716)) (False)
(assert (not (= x 59716)))

; Query: ((== x 59717)) (False)
(assert (not (not (= x 59717))))

(check-sat)
(get-model)
