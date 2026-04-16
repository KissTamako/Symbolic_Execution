(set-logic ALL)
; Constraint ID: b64642b37d5c5339
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60439)) (False)
(assert (not (not (= x 60439))))

(check-sat)
(get-model)
