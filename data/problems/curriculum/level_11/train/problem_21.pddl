

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b12)
(on b3 b11)
(on b4 b5)
(on b5 b2)
(on-table b6)
(on-table b7)
(on b8 b13)
(on b9 b6)
(on b10 b3)
(on b11 b9)
(on b12 b8)
(on b13 b10)
(clear b1)
(clear b4)
)
(:goal
(and
(on b2 b3)
(on b3 b12)
(on b4 b10)
(on b6 b9)
(on b7 b4)
(on b8 b1)
(on b9 b11)
(on b10 b13))
)
)


