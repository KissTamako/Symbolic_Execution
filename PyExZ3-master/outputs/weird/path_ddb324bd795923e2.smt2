(set-logic ALL)
; Executed Path ID: ddb324bd795923e2
; Generated at: 2026-04-17 03:12:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const x Int)
(declare-const y Int)

; ((== (+ (< x y) x) 1)) (True)
(assert (= (+ (< x y) x) 1))

(check-sat)
(get-model)
