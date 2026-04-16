(set-logic ALL)
; Constraint ID: 77da26454820ef13
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60691)) (False)
(assert (not (= x 60691)))

; Query: ((== x 60692)) (False)
(assert (not (not (= x 60692))))

(check-sat)
(get-model)
