(set-logic ALL)
; Constraint ID: b4fcf412b706c591
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60001)) (False)
(assert (not (= x 60001)))

; Query: ((== x 60002)) (False)
(assert (not (not (= x 60002))))

(check-sat)
(get-model)
