(set-logic ALL)
; Path ID: b30f6237af7b0f0e
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59236)) (False)
(assert (not (not (= x 59236))))

(check-sat)
(get-model)
