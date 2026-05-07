

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b7)
(ontable b3)
(on b4 b1)
(ontable b5)
(on b6 b10)
(on b7 b6)
(on b8 b5)
(ontable b9)
(on b10 b8)
(on b11 b9)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b10)
(on b3 b5)
(on b4 b9)
(on b6 b7)
(on b7 b8)
(on b8 b11)
(on b9 b1)
(on b11 b3))
)
)


