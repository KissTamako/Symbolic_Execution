(set-logic ALL)
; Constraint ID: bf1cef3ce1045a45
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60238)) (False)
(assert (not (= x 60238)))

; Query: ((== x 60239)) (False)
(assert (not (not (= x 60239))))

(check-sat)
(get-model)
