(set-logic ALL)
; Constraint ID: 491c00dede23bfac
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60298)) (False)
(assert (not (not (= x 60298))))

(check-sat)
(get-model)
