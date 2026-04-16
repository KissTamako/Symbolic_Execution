(set-logic ALL)
; Constraint ID: 1133bb043b8fe945
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60016)) (False)
(assert (not (= x 60016)))

; Query: ((== x 60017)) (False)
(assert (not (not (= x 60017))))

(check-sat)
(get-model)
