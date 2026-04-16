(set-logic ALL)
; Constraint ID: f3e527f3f011bcd4
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59869)) (False)
(assert (not (= x 59869)))

; Query: ((== x 59870)) (False)
(assert (not (not (= x 59870))))

(check-sat)
(get-model)
