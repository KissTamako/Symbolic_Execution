(set-logic ALL)
; Constraint ID: 35d3e5e1fc39cf46
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60538)) (False)
(assert (not (= x 60538)))

; Query: ((== x 60539)) (False)
(assert (not (not (= x 60539))))

(check-sat)
(get-model)
