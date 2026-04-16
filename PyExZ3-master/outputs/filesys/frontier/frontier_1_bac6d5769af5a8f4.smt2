(set-logic ALL)
; Constraint ID: bac6d5769af5a8f4
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60436)) (False)
(assert (not (= x 60436)))

; Query: ((== x 60437)) (False)
(assert (not (not (= x 60437))))

(check-sat)
(get-model)
