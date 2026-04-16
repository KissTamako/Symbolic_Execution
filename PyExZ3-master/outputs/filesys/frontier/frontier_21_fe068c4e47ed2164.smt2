(set-logic ALL)
; Frontier Constraint ID: fe068c4e47ed2164
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1717)) (False)
(assert (not (= x 1717)))

; Query: ((== x 1718)) (False)
(assert (not (not (= x 1718))))

(check-sat)
(get-model)
