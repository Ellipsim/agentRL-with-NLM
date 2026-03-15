

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b11)
(on-table b3)
(on b4 b1)
(on b5 b7)
(on b6 b8)
(on b7 b6)
(on b8 b12)
(on-table b9)
(on b10 b2)
(on-table b11)
(on b12 b3)
(clear b4)
(clear b5)
(clear b10)
)
(:goal
(and
(on b2 b7)
(on b3 b11)
(on b4 b6)
(on b7 b1)
(on b8 b5)
(on b9 b4)
(on b10 b9)
(on b11 b2)
(on b12 b10))
)
)


