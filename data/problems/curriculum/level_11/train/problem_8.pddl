

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on b2 b10)
(on b3 b9)
(on b4 b6)
(on b5 b4)
(on b6 b11)
(on b7 b12)
(on b8 b5)
(on b9 b2)
(on b10 b1)
(on b11 b3)
(on b12 b8)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b2 b9)
(on b3 b2)
(on b4 b1)
(on b5 b12)
(on b7 b6)
(on b8 b3)
(on b9 b11)
(on b10 b7)
(on b11 b5)
(on b12 b10))
)
)


