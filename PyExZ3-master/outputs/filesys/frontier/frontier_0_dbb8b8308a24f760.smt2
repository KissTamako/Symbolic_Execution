(set-logic ALL)
; Constraint ID: dbb8b8308a24f760
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59911)) (False)
(assert (not (not (= x 59911))))

(check-sat)
(get-model)
