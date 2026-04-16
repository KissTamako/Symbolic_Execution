(set-logic ALL)
; Constraint ID: 835436ebac08cb8e
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60004)) (False)
(assert (not (not (= x 60004))))

(check-sat)
(get-model)
