(set-logic ALL)
; Constraint ID: 02b20c03c9c1a503
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59701)) (False)
(assert (not (= x 59701)))

; Query: ((== x 59702)) (False)
(assert (not (not (= x 59702))))

(check-sat)
(get-model)
