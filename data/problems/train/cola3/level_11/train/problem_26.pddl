

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(on b4 b1)
(ontable b5)
(on b6 b8)
(on b7 b4)
(on b8 b12)
(on b9 b6)
(on b10 b5)
(ontable b11)
(on b12 b3)
(clear b7)
(clear b9)
(clear b10)
(clear b11)
)
(:goal
(and
(on b2 b4)
(on b3 b10)
(on b4 b8)
(on b5 b11)
(on b6 b5)
(on b7 b1)
(on b8 b6)
(on b9 b2)
(on b10 b7))
)
)


