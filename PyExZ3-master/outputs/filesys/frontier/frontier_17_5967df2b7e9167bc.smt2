(set-logic ALL)
; Constraint ID: 5967df2b7e9167bc
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60235)) (False)
(assert (not (= x 60235)))

; Query: ((== x 60236)) (False)
(assert (not (not (= x 60236))))

(check-sat)
(get-model)
