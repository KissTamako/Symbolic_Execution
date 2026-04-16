(set-logic ALL)
; Frontier Constraint ID: f2563acc907dfb63
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2536)) (False)
(assert (not (= x 2536)))

; Query: ((== x 2537)) (False)
(assert (not (not (= x 2537))))

(check-sat)
(get-model)
