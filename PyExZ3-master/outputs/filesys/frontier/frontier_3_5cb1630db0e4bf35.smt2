(set-logic ALL)
; Constraint ID: 5cb1630db0e4bf35
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60364)) (False)
(assert (not (= x 60364)))

; Query: ((== x 60365)) (False)
(assert (not (not (= x 60365))))

(check-sat)
(get-model)
