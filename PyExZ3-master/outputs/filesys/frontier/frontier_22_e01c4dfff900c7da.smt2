(set-logic ALL)
; Constraint ID: e01c4dfff900c7da
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60394)) (False)
(assert (not (not (= x 60394))))

(check-sat)
(get-model)
