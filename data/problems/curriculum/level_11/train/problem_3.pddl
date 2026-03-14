

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b7)
(on b2 b9)
(on b3 b1)
(on b4 b8)
(on b5 b12)
(on-table b6)
(on b7 b4)
(on b8 b6)
(on-table b9)
(on b10 b5)
(on b11 b10)
(on b12 b3)
(clear b2)
(clear b11)
)
(:goal
(and
(on b3 b11)
(on b4 b2)
(on b6 b7)
(on b7 b4)
(on b8 b12)
(on b9 b6)
(on b10 b9)
(on b11 b5)
(on b12 b10))
)
)


