

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b11)
(ontable b2)
(on b3 b2)
(on b4 b10)
(on b5 b8)
(ontable b6)
(on b7 b6)
(on b8 b3)
(on b9 b4)
(on b10 b5)
(on b11 b7)
(clear b1)
(clear b9)
)
(:goal
(and
(on b1 b11)
(on b4 b3)
(on b5 b4)
(on b6 b7)
(on b8 b10)
(on b9 b2)
(on b10 b1)
(on b11 b5))
)
)


