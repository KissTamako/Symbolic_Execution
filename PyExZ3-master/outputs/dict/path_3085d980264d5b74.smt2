(set-logic ALL)
; Executed Path ID: 3085d980264d5b74
; Generated at: 2026-04-16 16:02:52
; Solver: Z3Wrapper
; Number of predicates: 4
; Has query: False

(declare-const x Int)

; ((== x 4)) (False)
(assert (not (= x 4)))
; ((== x 101)) (False)
(assert (not (= x 101)))
; ((== x 1)) (True)
(assert (= x 1))
; ((== x 1)) (True)
(assert (= x 1))

(check-sat)
(get-model)
