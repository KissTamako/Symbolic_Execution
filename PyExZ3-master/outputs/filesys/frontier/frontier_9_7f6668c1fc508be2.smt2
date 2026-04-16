(set-logic ALL)
; Constraint ID: 7f6668c1fc508be2
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60523)) (False)
(assert (not (= x 60523)))

; Query: ((== x 60524)) (False)
(assert (not (not (= x 60524))))

(check-sat)
(get-model)
