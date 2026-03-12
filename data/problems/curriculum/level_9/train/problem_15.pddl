

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b7)
(on b3 b10)
(on-table b4)
(on-table b5)
(on b6 b5)
(on-table b7)
(on-table b8)
(on b9 b3)
(on b10 b6)
(on b11 b4)
(clear b1)
(clear b2)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b8)
(on b2 b5)
(on b4 b11)
(on b5 b6)
(on b6 b7)
(on b7 b1)
(on b8 b9)
(on b9 b3)
(on b10 b2)
(on b11 b10))
)
)


