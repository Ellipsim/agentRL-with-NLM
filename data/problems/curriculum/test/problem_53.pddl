

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b5)
(on b3 b2)
(on-table b4)
(on b5 b9)
(on b6 b3)
(on b7 b10)
(on b8 b4)
(on b9 b7)
(on-table b10)
(on b11 b1)
(clear b8)
(clear b11)
)
(:goal
(and
(on b2 b8)
(on b4 b10)
(on b5 b9)
(on b6 b3)
(on b7 b5)
(on b8 b1)
(on b9 b4)
(on b10 b6)
(on b11 b7))
)
)


