(set-logic ALL)
; Constraint ID: 5bd6f26d06b6d970
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60529)) (False)
(assert (not (= x 60529)))

; Query: ((== x 60530)) (False)
(assert (not (not (= x 60530))))

(check-sat)
(get-model)
