(set-logic ALL)
; Constraint ID: 0887eb16549fa4a0
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59935)) (False)
(assert (not (= x 59935)))

; Query: ((== x 59936)) (False)
(assert (not (not (= x 59936))))

(check-sat)
(get-model)
