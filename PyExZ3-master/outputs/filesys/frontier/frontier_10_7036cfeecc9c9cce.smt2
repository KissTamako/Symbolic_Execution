(set-logic ALL)
; Constraint ID: 7036cfeecc9c9cce
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59926)) (False)
(assert (not (not (= x 59926))))

(check-sat)
(get-model)
