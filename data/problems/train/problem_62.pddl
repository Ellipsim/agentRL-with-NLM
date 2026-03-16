

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b11)
(ontable b3)
(on b4 b3)
(on b5 b6)
(ontable b6)
(on b7 b8)
(on b8 b5)
(on b9 b7)
(on b10 b2)
(ontable b11)
(clear b1)
(clear b4)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b2 b7)
(on b3 b1)
(on b4 b5)
(on b5 b9)
(on b6 b3)
(on b8 b6)
(on b10 b4)
(on b11 b10))
)
)


