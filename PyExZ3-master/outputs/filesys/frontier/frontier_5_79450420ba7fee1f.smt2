(set-logic ALL)
; Constraint ID: 79450420ba7fee1f
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60592)) (False)
(assert (not (= x 60592)))

; Query: ((== x 60593)) (False)
(assert (not (not (= x 60593))))

(check-sat)
(get-model)
