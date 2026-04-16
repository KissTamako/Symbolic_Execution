(set-logic ALL)
; Frontier Constraint ID: c377297ca9bb21b8
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1708)) (False)
(assert (not (= x 1708)))

; Query: ((== x 1709)) (False)
(assert (not (not (= x 1709))))

(check-sat)
(get-model)
